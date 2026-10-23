"""Tests unitaires du modèle :class:`models.vehicule.Vehicule`."""

import pytest

from models.route import Route
from models.vehicule import Vehicule


def test_initialisation_conserve_les_attributs():
    route = Route("A1", 10, 80)
    vehicule = Vehicule(position=1.5, vitesse=42, route_actuelle=route, identifiant="V1")

    assert vehicule.position == 1.5
    assert vehicule.vitesse == 42
    assert vehicule.route_actuelle is route
    assert vehicule.identifiant == "V1"


def test_avancer_sans_route_ne_fait_rien():
    vehicule = Vehicule(position=1.0, vitesse=50, route_actuelle=None, identifiant="V1")

    assert vehicule.avancer(delta_t=10) == 0.0
    assert vehicule.position == 1.0


def test_avancer_calcule_la_distance_parcourue():
    route = Route("A1", 100, 80)
    vehicule = Vehicule(position=1.0, vitesse=60, route_actuelle=route, identifiant="V1")

    distance = vehicule.avancer(delta_t=30)

    assert distance == pytest.approx(30.0)
    assert vehicule.position == pytest.approx(31.0)
    assert vehicule.route_actuelle is route


def test_avancer_avec_vitesse_negative_ne_recule_pas():
    route = Route("A1", 10, 80)
    vehicule = Vehicule(position=1.0, vitesse=-20, route_actuelle=route, identifiant="V1")

    assert vehicule.avancer(delta_t=10) == 0.0
    assert vehicule.position == 1.0


def test_avancer_au_dela_de_la_route_la_quitte():
    route = Route("A1", 5, 80)
    vehicule = Vehicule(position=4.0, vitesse=120, route_actuelle=route, identifiant="V1")

    distance = vehicule.avancer(delta_t=60)

    assert distance == pytest.approx(1.0)
    assert vehicule.position == 5
    assert vehicule.route_actuelle is None


def test_changer_de_route_reinitialise_la_position():
    route_a = Route("A1", 10, 80)
    route_b = Route("B2", 12, 60)
    vehicule = Vehicule(position=4.0, vitesse=50, route_actuelle=route_a, identifiant="V1")

    resultat = vehicule.changer_de_route(route_b)

    assert resultat is route_b
    assert vehicule.route_actuelle is route_b
    assert vehicule.position == 0
