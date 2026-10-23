"""Tests unitaires de :func:`out.export.exporter_statistiques`."""

import json

from out.export import exporter_statistiques


def test_export_ecrit_le_json(tmp_path):
    statistiques = [{"tour": 1, "vitesse_moyenne": 42.5}, {"tour": 2, "vitesse_moyenne": 38.0}]
    fichier = tmp_path / "resultats.json"

    chemin = exporter_statistiques(statistiques, str(fichier))

    assert chemin == fichier
    assert json.loads(fichier.read_text(encoding="utf-8")) == statistiques


def test_export_cree_le_dossier_parent(tmp_path):
    fichier = tmp_path / "sous" / "dossier" / "resultats.json"

    exporter_statistiques([], str(fichier))

    assert fichier.exists()
    assert json.loads(fichier.read_text(encoding="utf-8")) == []
