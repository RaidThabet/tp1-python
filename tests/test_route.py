"""Tests unitaires du modèle :class:`models.route.Route`."""

import pytest

from models.route import Route
from models.vehicule import Vehicule


def test_initialisation_attribue_la_route_aux_vehicules():
    route = Route("A1", 10, 80)
    vehicule = Vehicule(0.5, 30, None, "V1")

    route = Route("A1", 10, 80, vehicules=[vehicule])

    assert route.nom == "A1"
    assert route.longueur == 10
    assert route.limite_vitesse == 80
    assert vehicule.route_actuelle is route
    assert vehicule in route.vehicules


def test_ajouter_vehicule_evite_les_doublons():
    route = Route("A1", 10, 80)
    vehicule = Vehicule(0.5, 30, None, "V1")

    route.ajouter_vehicule(vehicule)
    route.ajouter_vehicule(vehicule)

    assert route.vehicules == [vehicule]
    assert vehicule.route_actuelle is route


def test_mise_a_jour_borne_les_vitesses_a_la_limite():
    route = Route("A1", 10, 60)
    vehicule = Vehicule(0.0, 200, route, "V1")
    route.ajouter_vehicule(vehicule)

    route.mettre_a_jour_vehicules(delta_t=1, tour=0)

    assert 4.0 <= vehicule.vitesse <= route.limite_vitesse


def test_mise_a_jour_deplace_les_vehicules():
    route = Route("A1", 100, 60)
    vehicule = Vehicule(0.0, 60, route, "V1")
    route.ajouter_vehicule(vehicule)

    route.mettre_a_jour_vehicules(delta_t=60, tour=1)

    assert vehicule.position > 0
    assert vehicule in route.vehicules


def test_mise_a_jour_retire_les_vehicules_arrives():
    route = Route("A1", 1, 50)
    vehicule = Vehicule(0.9, 50, route, "V1")
    route.ajouter_vehicule(vehicule)

    restants = route.mettre_a_jour_vehicules(delta_t=60, tour=1)

    assert restants == []
    assert route.vehicules == []
    assert vehicule.route_actuelle is None
    assert vehicule.position == route.longueur


def test_mise_a_jour_reduit_la_vitesse_quand_la_route_est_dense():
    route = Route("A1", 1, 100)
    vehicules = [Vehicule(0.0, 100, route, f"V{i}") for i in range(5)]
    for vehicule in vehicules:
        route.ajouter_vehicule(vehicule)

    route.mettre_a_jour_vehicules(delta_t=0, tour=0, pression_reseau=1.0)

    assert all(vehicule.vitesse < 100 for vehicule in vehicules)


def test_mise_a_jour_sur_route_vide():
    route = Route("A1", 10, 60)

    assert route.mettre_a_jour_vehicules() == []
