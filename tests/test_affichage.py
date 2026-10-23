"""Tests unitaires de :func:`out.affichage.afficher_statistiques`."""

from out.affichage import afficher_statistiques


def test_affichage_sans_statistiques(capsys):
    afficher_statistiques([])

    assert capsys.readouterr().out.strip() == "Aucune statistique disponible."
