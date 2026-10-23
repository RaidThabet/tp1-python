"""Modèle représentant un véhicule circulant sur une route."""


class Vehicule:
    """Véhicule évoluant sur une route du réseau routier.

    Un véhicule possède une position (en kilomètres depuis le début de sa
    route), une vitesse (en km/h), une route actuelle et un identifiant unique.

    Attributes:
        position: Position courante sur la route, en kilomètres.
        vitesse: Vitesse courante du véhicule, en km/h.
        route_actuelle: Route sur laquelle circule le véhicule, ou ``None``
            lorsqu'il a quitté le réseau.
        identifiant: Identifiant unique du véhicule (par exemple ``"V1"``).
    """

    def __init__(self, position, vitesse, route_actuelle, identifiant):
        """Initialise un véhicule.

        Args:
            position: Position initiale sur la route, en kilomètres.
            vitesse: Vitesse initiale, en km/h.
            route_actuelle: Route sur laquelle le véhicule circule.
            identifiant: Identifiant unique du véhicule.
        """
        self.position = position
        self.vitesse = vitesse
        self.route_actuelle = route_actuelle
        self.identifiant = identifiant

    def avancer(self, delta_t=1):
        """Déplace le véhicule sur sa route actuelle en fonction de sa vitesse.

        Le véhicule est bloqué à l'extrémité de la route lorsqu'il la dépasse ;
        sa ``route_actuelle`` est alors mise à ``None``.

        Args:
            delta_t: Durée écoulée depuis le dernier déplacement, en minutes.

        Returns:
            Distance réellement parcourue pendant ``delta_t``, en kilomètres.
        """
        if self.route_actuelle is None:
            return 0.0

        distance_km = max(self.vitesse, 0) * (delta_t / 60)
        nouvelle_position = self.position + distance_km
        limite_route = self.route_actuelle.longueur

        if nouvelle_position >= limite_route:
            distance_restante = limite_route - self.position
            self.position = limite_route
            self.route_actuelle = None
            return max(distance_restante, 0.0)

        self.position = nouvelle_position
        return distance_km

    def changer_de_route(self, nouvelle_route):
        """Fait passer le véhicule sur une nouvelle route.

        Args:
            nouvelle_route: Route de destination.

        Returns:
            La nouvelle route attribuée au véhicule.
        """
        self.route_actuelle = nouvelle_route
        self.position = 0
        return nouvelle_route
