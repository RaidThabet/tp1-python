"""Tests unitaires de :class:`core.analyseur.Analyseur`."""

import pytest

from core.analyseur import Analyseur
from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


def test_vitesse_moyenne_ignore_les_vehicules_inactifs():
    analyseur = Analyseur()
    route = Route("A1", 10, 80)
    actifs = [
        Vehicule(0.0, 40, route, "V1"),
        Vehicule(1.0, 60, route, "V2"),
    ]
    inactif = Vehicule(9.0, 100, None, "V3")

    assert analyseur.calc_vitesse_moyenne(actifs + [inactif]) == pytest.approx(50.0)


def test_vitesse_moyenne_sans_vehicule_actif():
    analyseur = Analyseur()

    assert analyseur.calc_vitesse_moyenne([]) == 0.0
    assert analyseur.calc_vitesse_moyenne([Vehicule(0, 50, None, "V1")]) == 0.0


def test_zones_congestion_detecte_les_routes_lentes():
    analyseur = Analyseur()
    reseau = ReseauRoutier()
    route = Route("A1", 10, 100)
    route.ajouter_vehicule(Vehicule(0.0, 40, route, "V1"))
    route.ajouter_vehicule(Vehicule(1.0, 50, route, "V2"))
    reseau.ajouter_route(route)

    zones = analyseur.calc_zones_congestion(reseau)

    assert len(zones) == 1
    assert zones[0]["route"] == "A1"
    assert zones[0]["vitesse_moyenne"] == pytest.approx(45.0)
    assert zones[0]["seuil_congestion"] == pytest.approx(60.0)
    assert zones[0]["nb_vehicules"] == 2


def test_zones_congestion_ignore_les_routes_fluides_et_vides():
    analyseur = Analyseur()
    reseau = ReseauRoutier()
    fluide = Route("A1", 10, 100)
    fluide.ajouter_vehicule(Vehicule(0.0, 90, fluide, "V1"))
    vide = Route("B2", 10, 100)
    reseau.ajouter_route(fluide)
    reseau.ajouter_route(vide)

    assert analyseur.calc_zones_congestion(reseau) == []


def test_zones_congestion_sans_reseau():
    analyseur = Analyseur()

    assert analyseur.calc_zones_congestion(ReseauRoutier()) == []
    assert analyseur.calc_zones_congestion(object()) == []


def test_temps_parcours():
    analyseur = Analyseur()
    route = Route("A1", 10, 80)
    vehicule = Vehicule(4.0, 60, route, "V1")

    assert analyseur.calc_temps_parcours(vehicule) == pytest.approx(6.0)


def test_temps_parcours_sans_route_ou_route_nulle():
    analyseur = Analyseur()

    assert analyseur.calc_temps_parcours(Vehicule(0, 60, None, "V1")) == 0.0
    assert analyseur.calc_temps_parcours(Vehicule(0, 60, Route("A1", 0, 80), "V2")) == 0.0
