"""Tests unitaires du modèle :class:`models.reseau.ReseauRoutier`."""

from models.reseau import ReseauRoutier
from models.route import Route


def test_ajouter_route_evite_les_doublons():
    reseau = ReseauRoutier()
    route = Route("A1", 10, 80)

    reseau.ajouter_route(route)
    reseau.ajouter_route(route)

    assert reseau.routes == [route]


def test_obtenir_route_par_nom():
    reseau = ReseauRoutier()
    route_a = Route("A1", 10, 80)
    route_b = Route("B2", 12, 60)
    reseau.ajouter_route(route_a)
    reseau.ajouter_route(route_b)

    assert reseau.obtenir_route_par_nom("B2") is route_b
    assert reseau.obtenir_route_par_nom("inconnue") is None


def test_ajouter_intersection():
    reseau = ReseauRoutier()
    intersection = {"nom": "I1", "coordonnees": (0, 0)}

    reseau.ajouter_intersection(intersection)
    reseau.ajouter_intersection(intersection)

    assert reseau.intersections == [intersection, intersection]


def test_afficher_reseau(capsys):
    reseau = ReseauRoutier()
    reseau.ajouter_route(Route("A1", 10, 80))
    reseau.ajouter_intersection({"nom": "I1", "coordonnees": (1, 2)})

    reseau.afficher_reseau()

    sortie = capsys.readouterr().out
    assert "Réseau Routier:" in sortie
    assert "Route: A1, Longueur: 10 km" in sortie
    assert "Intersection: I1, Coordonnées: (1, 2)" in sortie
