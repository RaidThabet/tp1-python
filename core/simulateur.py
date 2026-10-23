"""Moteur de simulation de trafic routier.

Le module fournit la classe :class:`Simulateur`, qui charge une configuration
de réseau, injecte des véhicules au fil des tours et collecte des statistiques
d'évolution (vitesses, congestion, pression réseau).
"""

import json
import math
from pathlib import Path

from core.analyseur import Analyseur
from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


class Simulateur:
    """Orchestre la simulation d'un réseau routier sur plusieurs tours.

    Attributes:
        fichier_config: Chemin du fichier JSON de configuration, ou ``None``
            pour utiliser la configuration par défaut.
        reseau: Réseau routier simulé.
        vehicules: Liste de tous les véhicules créés depuis le début.
        analyseur: Analyseur calculant les statistiques.
        statistiques: Statistiques produites par le dernier lancement.
    """

    def __init__(self, fichier_config=None):
        """Initialise le simulateur et charge la configuration.

        Args:
            fichier_config: Chemin (absolu ou relatif à la racine du projet)
                du fichier JSON de configuration. Si omis ou introuvable, la
                configuration par défaut est utilisée.
        """
        self.fichier_config = fichier_config
        self.reseau = ReseauRoutier()
        self.vehicules = []
        self.analyseur = Analyseur()
        self.statistiques = []
        self._compteur_vehicules = 1
        self._charger_config()

    def _charger_config(self):
        """Charge le réseau depuis ``fichier_config`` ou la configuration par défaut."""
        if not self.fichier_config:
            self._config_par_defaut()
            return

        chemin = Path(self.fichier_config)
        if not chemin.is_absolute():
            chemin = Path(__file__).resolve().parents[1] / chemin

        if not chemin.exists():
            self._config_par_defaut()
            return

        with chemin.open("r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)

        for route_data in donnees.get("routes", []):
            route = Route(
                nom=route_data.get("nom", "Route"),
                longueur=route_data.get("longueur", 0),
                limite_vitesse=route_data.get("limite_vitesse", 50),
            )
            for vehicule_data in route_data.get("vehicules", []):
                vehicule = Vehicule(
                    position=vehicule_data.get("position", 0),
                    vitesse=vehicule_data.get("vitesse", 0),
                    route_actuelle=route,
                    identifiant=vehicule_data.get("identifiant", f"V-{len(self.vehicules) + 1}"),
                )
                route.ajouter_vehicule(vehicule)
                self.vehicules.append(vehicule)
            self.reseau.ajouter_route(route)

        for intersection in donnees.get("intersections", []):
            self.reseau.ajouter_intersection(intersection)
        self._synchroniser_compteur_vehicules()

    def _config_par_defaut(self):
        """Construit un réseau de démonstration avec trois routes et huit véhicules."""
        route_a = Route("A1", 12, 80)
        route_b = Route("B2", 16, 60)
        route_c = Route("C3", 10, 50)

        vehicules_initiaux = [
            Vehicule(0.3, 42, route_a, "V1"),
            Vehicule(1.2, 38, route_a, "V2"),
            Vehicule(2.1, 36, route_a, "V3"),
            Vehicule(0.4, 30, route_b, "V4"),
            Vehicule(1.0, 28, route_b, "V5"),
            Vehicule(2.4, 32, route_b, "V6"),
            Vehicule(0.2, 25, route_c, "V7"),
            Vehicule(0.9, 22, route_c, "V8"),
        ]

        for vehicule in vehicules_initiaux:
            vehicule.route_actuelle.ajouter_vehicule(vehicule)

        self.reseau.ajouter_route(route_a)
        self.reseau.ajouter_route(route_b)
        self.reseau.ajouter_route(route_c)
        self.reseau.ajouter_intersection({"nom": "I1", "coordonnees": (0, 0)})
        self.reseau.ajouter_intersection({"nom": "I2", "coordonnees": (5, 3)})

        self.vehicules = vehicules_initiaux
        self._synchroniser_compteur_vehicules()

    def _synchroniser_compteur_vehicules(self):
        """Aligne le compteur d'identifiants sur le plus grand suffixe numérique existant."""
        plus_grand_id = 0
        for vehicule in self.vehicules:
            suffixe = "".join(char for char in vehicule.identifiant if char.isdigit())
            if suffixe:
                plus_grand_id = max(plus_grand_id, int(suffixe))
        self._compteur_vehicules = plus_grand_id + 1

    def _pression_reseau(self):
        """Calcule la pression du réseau, ratio entre véhicules actifs et capacité.

        Returns:
            Pression normalisée, plafonnée à ``1.5``. Vaut ``0.0`` si le réseau
            n'a aucune capacité.
        """
        vehicules_actifs = sum(len(route.vehicules) for route in self.reseau.routes)
        capacite_reseau = sum(max(route.longueur * 1.3, 1.0) for route in self.reseau.routes)
        if capacite_reseau <= 0:
            return 0.0
        return min(1.5, vehicules_actifs / capacite_reseau)

    def _injecter_vehicules(self, tour):
        """Injecte de nouveaux véhicules sur les routes selon le flux du tour.

        L'intensité du flux suit une sinusoïde ; un véhicule est créé au début
        d'une route lorsque sa capacité n'est pas atteinte.

        Args:
            tour: Numéro du tour courant.
        """
        for indice_route, route in enumerate(self.reseau.routes):
            intensite_flux = 0.5 + 0.5 * math.sin((tour + indice_route * 4) / 7)
            intervalle = max(2, int(6 - intensite_flux * 3) + indice_route)
            capacite_route = max(8, int(route.longueur * 1.8))

            if len(route.vehicules) >= capacite_route or tour % intervalle != 0:
                continue

            identifiant = f"V{self._compteur_vehicules}"
            self._compteur_vehicules += 1
            vitesse_depart = route.limite_vitesse * (0.35 + 0.4 * intensite_flux)
            vehicule = Vehicule(0.0, vitesse_depart, route, identifiant)
            route.ajouter_vehicule(vehicule)
            self.vehicules.append(vehicule)

    def lancer_simulation(self, n_tours=60, delta_t=1):
        """Fait évoluer les véhicules et collecte les statistiques de la simulation.

        Args:
            n_tours: Nombre de tours à simuler.
            delta_t: Durée d'un tour, en minutes.

        Returns:
            La liste des statistiques, une entrée par tour. Chaque entrée
            contient le tour, les vitesses moyenne/min/max, les zones de
            congestion, le nombre de véhicules actifs et la pression réseau.
        """
        self.statistiques = []
        for tour in range(1, n_tours + 1):
            self._injecter_vehicules(tour)
            pression_reseau = self._pression_reseau()

            for indice_route, route in enumerate(self.reseau.routes):
                route.mettre_a_jour_vehicules(
                    delta_t=delta_t,
                    tour=tour,
                    pression_reseau=pression_reseau,
                    indice_route=indice_route,
                )

            vitesses_actives = [vehicule.vitesse for vehicule in self.vehicules if vehicule.route_actuelle is not None]
            vitesse_min = min(vitesses_actives) if vitesses_actives else 0.0
            vitesse_max = max(vitesses_actives) if vitesses_actives else 0.0
            zones_congestion = self.analyseur.calc_zones_congestion(self.reseau)

            stat = {
                "tour": tour,
                "delta_t": delta_t,
                "vitesse_moyenne": self.analyseur.calc_vitesse_moyenne(self.vehicules),
                "vitesse_min": vitesse_min,
                "vitesse_max": vitesse_max,
                "zones_congestion": zones_congestion,
                "routes_congestionnees": len(zones_congestion),
                "vehicules_actifs": len(vitesses_actives),
                "pression_reseau": pression_reseau,
            }
            self.statistiques.append(stat)

        return self.statistiques
