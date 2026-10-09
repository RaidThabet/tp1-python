class ReseauRoutier:
    def __init__(self):
        self.routes = []
        self.intersections = []

    def ajouter_route(self, route):
        self.routes.append(route)

    def ajouter_intersection(self, intersection):
        self.intersections.append(intersection)

    def afficher_reseau(self):
        print("Réseau Routier:")
        for route in self.routes:
            print(f"Route: {route.nom}, Longueur: {route.longueur} km")
        for intersection in self.intersections:
            print(f"Intersection: {intersection.nom}, Coordonnées: {intersection.coordonnees}")