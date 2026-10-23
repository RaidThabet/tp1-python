"""Analyseur de statistiques pour la simulation de trafic."""


class Analyseur:
    """Regroupe les calculs statistiques sur les véhicules et le réseau."""

    def calc_vitesse_moyenne(self, vehicules):
        """Calcule la vitesse moyenne des véhicules actifs.

        Les véhicules ayant quitté le réseau (``route_actuelle`` valant
        ``None``) sont ignorés.

        Args:
            vehicules: Itérable de véhicules.

        Returns:
            La vitesse moyenne en km/h, ou ``0.0`` si aucun véhicule n'est actif.
        """
        vehicules_actifs = [v for v in vehicules if getattr(v, "route_actuelle", None) is not None]
        if not vehicules_actifs:
            return 0.0
        return sum(v.vitesse for v in vehicules_actifs) / len(vehicules_actifs)

    def calc_zones_congestion(self, reseau):
        """Retourne les routes dont la vitesse moyenne est inférieure au seuil critique.

        Le seuil critique correspond à 60 % de la limite de vitesse de la route.

        Args:
            reseau: Réseau routier exposant un attribut ``routes``.

        Returns:
            Liste de dictionnaires décrivant chaque route congestionnée, avec
            son nom, sa vitesse moyenne, son seuil et son nombre de véhicules.
        """
        zones = []
        for route in getattr(reseau, "routes", []):
            if not route.vehicules:
                continue
            vitesse_moyenne = sum(v.vitesse for v in route.vehicules) / len(route.vehicules)
            seuil = route.limite_vitesse * 0.6
            if vitesse_moyenne < seuil:
                zones.append({
                    "route": route.nom,
                    "vitesse_moyenne": vitesse_moyenne,
                    "seuil_congestion": seuil,
                    "nb_vehicules": len(route.vehicules),
                })
        return zones

    def calc_temps_parcours(self, vehicule):
        """Calcule le temps de parcours restant en minutes pour un véhicule.

        Args:
            vehicule: Véhicule analysé.

        Returns:
            Le temps restant en minutes, ou ``0.0`` si le véhicule n'a pas de
            route ou si la route a une longueur nulle.
        """
        route = getattr(vehicule, "route_actuelle", None)
        if route is None or route.longueur <= 0:
            return 0.0
        distance_restante = max(route.longueur - vehicule.position, 0)
        vitesse = max(vehicule.vitesse, 0.01)
        return (distance_restante / vitesse) * 60
