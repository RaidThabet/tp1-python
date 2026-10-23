"""Modèle représentant une route et sa dynamique de circulation."""

import math


class Route:
    """Portion de route linéaire accueillant des véhicules.

    La route applique un modèle simplifié de suivi : chaque véhicule ajuste sa
    vitesse en fonction de l'espacement avec le véhicule précédent, de la
    densité de la route et de la pression globale du réseau.

    Attributes:
        nom: Nom de la route (par exemple ``"A1"``).
        longueur: Longueur de la route, en kilomètres.
        limite_vitesse: Vitesse maximale autorisée, en km/h.
        vehicules: Liste des véhicules actuellement présents sur la route.
    """

    def __init__(self, nom, longueur, limite_vitesse, vehicules=None):
        """Initialise une route.

        Args:
            nom: Nom de la route.
            longueur: Longueur de la route, en kilomètres.
            limite_vitesse: Vitesse maximale autorisée, en km/h.
            vehicules: Véhicules initialement présents sur la route. Par
                défaut, la route est vide.
        """
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.vehicules = list(vehicules) if vehicules is not None else []
        for vehicule in self.vehicules:
            vehicule.route_actuelle = self

    def ajouter_vehicule(self, vehicule):
        """Ajoute un véhicule à la route s'il n'y est pas déjà.

        La ``route_actuelle`` du véhicule est systématiquement mise à jour.

        Args:
            vehicule: Véhicule à ajouter.
        """
        if vehicule not in self.vehicules:
            self.vehicules.append(vehicule)
        vehicule.route_actuelle = self

    def mettre_a_jour_vehicules(self, delta_t=1, tour=0, pression_reseau=0.0, indice_route=0):
        """Met à jour les vitesses puis déplace les véhicules de la route.

        Les véhicules sont triés par position, leur vitesse cible est recalculée
        selon l'espacement, une onde de circulation sinusoïdale, la densité de
        la route et la pression du réseau. Les véhicules ayant atteint la fin
        de la route en sont retirés.

        Args:
            delta_t: Durée écoulée depuis le dernier tour, en minutes.
            tour: Numéro du tour courant, utilisé pour l'onde de circulation.
            pression_reseau: Pression globale du réseau, entre 0 et 1.5.
            indice_route: Indice de la route dans le réseau, utilisé pour
                décaler l'onde de circulation.

        Returns:
            La liste des véhicules encore présents sur la route après mise à jour.
        """
        vehicules_tries = sorted(self.vehicules, key=lambda vehicule: vehicule.position)
        densite = len(vehicules_tries) / max(self.longueur, 1)

        for position, vehicule in enumerate(vehicules_tries):
            vehicule_suivant = vehicules_tries[position + 1] if position + 1 < len(vehicules_tries) else None
            if vehicule_suivant is None:
                espacement = self.longueur - vehicule.position
            else:
                espacement = max(vehicule_suivant.position - vehicule.position, 0.0)

            pression_espacement = max(0.0, min(1.0, (2.5 - espacement) / 2.5))
            onde_circulation = 0.72 + 0.28 * math.sin((tour + indice_route * 3 + position) / 4)
            freinage_densite = min(0.75, densite * 0.24 + pression_reseau * 0.35)
            cible = self.limite_vitesse * onde_circulation * (1 - freinage_densite) * (1 - 0.8 * pression_espacement)
            cible = max(6.0, min(self.limite_vitesse, cible))

            vehicule.vitesse += (cible - vehicule.vitesse) * 0.45
            vehicule.vitesse = max(4.0, min(self.limite_vitesse, vehicule.vitesse))

        for vehicule in list(self.vehicules):
            vehicule.avancer(delta_t)
            if vehicule.position >= self.longueur:
                vehicule.position = self.longueur
                vehicule.route_actuelle = None
                self.vehicules.remove(vehicule)
        return self.vehicules
