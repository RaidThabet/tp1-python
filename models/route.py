class Route:
    def __init__(self, nom, longueur, limite_vitesse, vehicules=None):
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.vehicules = vehicules if vehicules is not None else []

    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def mettre_a_jour_vehicules(self):
        pass
    