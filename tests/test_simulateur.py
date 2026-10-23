"""Tests unitaires de :class:`core.simulateur.Simulateur`."""

import json

import pytest

from core.simulateur import Simulateur


def test_configuration_par_defaut():
    simulateur = Simulateur()

    assert [route.nom for route in simulateur.reseau.routes] == ["A1", "B2", "C3"]
    assert len(simulateur.vehicules) == 8
    assert len(simulateur.reseau.intersections) == 2
    assert simulateur._compteur_vehicules == 9


def test_fichier_de_configuration_introuvable_utilise_le_defaut():
    simulateur = Simulateur("/chemin/inexistant/config.json")

    assert len(simulateur.reseau.routes) == 3
    assert len(simulateur.vehicules) == 8


def test_chargement_configuration_relative_au_projet():
    simulateur = Simulateur("data/config_reseau.json")

    assert [route.nom for route in simulateur.reseau.routes] == ["A1", "B2", "C3"]
    assert len(simulateur.vehicules) == 3
    assert [intersection["nom"] for intersection in simulateur.reseau.intersections] == ["I1", "I2", "I3"]


def test_chargement_configuration_personnalisee(tmp_path):
    configuration = {
        "routes": [
            {
                "nom": "X1",
                "longueur": 5,
                "limite_vitesse": 50,
                "vehicules": [{"identifiant": "V7", "position": 1, "vitesse": 10}],
            }
        ],
        "intersections": [{"nom": "I1", "coordonnees": [0, 0]}],
    }
    fichier = tmp_path / "config.json"
    fichier.write_text(json.dumps(configuration), encoding="utf-8")

    simulateur = Simulateur(str(fichier))

    route = simulateur.reseau.obtenir_route_par_nom("X1")
    assert route is not None
    assert route.longueur == 5
    assert len(route.vehicules) == 1
    assert simulateur.vehicules[0].identifiant == "V7"
    assert simulateur.vehicules[0].route_actuelle is route
    assert simulateur._compteur_vehicules == 8


def test_pression_reseau_bornee():
    simulateur = Simulateur()

    pression = simulateur._pression_reseau()

    assert 0.0 <= pression <= 1.5


def test_injection_vehicules_au_tour_adéquat():
    simulateur = Simulateur()
    vehicules_avant = len(simulateur.vehicules)

    simulateur._injecter_vehicules(6)

    assert len(simulateur.vehicules) == vehicules_avant + 1
    assert simulateur.vehicules[-1].identifiant == "V9"


def test_lancer_simulation_collecte_les_statistiques():
    simulateur = Simulateur()

    statistiques = simulateur.lancer_simulation(n_tours=10, delta_t=2)

    assert len(statistiques) == 10
    assert [stat["tour"] for stat in statistiques] == list(range(1, 11))
    for stat in statistiques:
        assert stat["delta_t"] == 2
        assert stat["vitesse_min"] <= stat["vitesse_moyenne"] <= stat["vitesse_max"]
        assert stat["vehicules_actifs"] >= 0
        assert 0.0 <= stat["pression_reseau"] <= 1.5
        assert stat["routes_congestionnees"] == len(stat["zones_congestion"])


def test_lancer_simulation_reinitialise_les_statistiques():
    simulateur = Simulateur()

    simulateur.lancer_simulation(n_tours=5)
    statistiques = simulateur.lancer_simulation(n_tours=3)

    assert len(statistiques) == 3
    assert len(simulateur.statistiques) == 3
    assert statistiques is simulateur.statistiques


def test_simulation_sans_tour():
    simulateur = Simulateur()

    assert simulateur.lancer_simulation(n_tours=0) == []
