"""Modèle représentant le réseau routier global."""


class ReseauRoutier:
    """Conteneur des routes et des intersections d'un réseau routier.

    Attributes:
        routes: Liste des routes du réseau.
        intersections: Liste des intersections, sous forme de dictionnaires ou
            d'objets exposant les attributs ``nom`` et ``coordonnees``.
    """

    def __init__(self):
        """Initialise un réseau routier vide."""
        self.routes = []
        self.intersections = []

    def ajouter_route(self, route):
        """Ajoute une route au réseau si elle n'y est pas déjà.

        Args:
            route: Route à ajouter.
        """
        if route not in self.routes:
            self.routes.append(route)

    def ajouter_intersection(self, intersection):
        """Ajoute une intersection au réseau.

        Args:
            intersection: Intersection à ajouter (dictionnaire ou objet).
        """
        self.intersections.append(intersection)

    def obtenir_route_par_nom(self, nom):
        """Recherche une route par son nom.

        Args:
            nom: Nom de la route recherchée.

        Returns:
            La première route portant ce nom, ou ``None`` si aucune ne correspond.
        """
        for route in self.routes:
            if route.nom == nom:
                return route
        return None

    def afficher_reseau(self):
        """Affiche sur la sortie standard la description du réseau."""
        print("Réseau Routier:")
        for route in self.routes:
            print(f"Route: {route.nom}, Longueur: {route.longueur} km")
        for intersection in self.intersections:
            nom = intersection.get("nom", "Intersection") if isinstance(intersection, dict) else getattr(intersection, "nom", "Intersection")
            coordonnees = intersection.get("coordonnees", (0, 0)) if isinstance(intersection, dict) else getattr(intersection, "coordonnees", (0, 0))
            print(f"Intersection: {nom}, Coordonnées: {coordonnees}")
