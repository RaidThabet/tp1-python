"""Export des statistiques de simulation au format JSON."""

import json
from pathlib import Path


def exporter_statistiques(statistiques, fichier="out/resultats.json"):
    """Écrit les statistiques dans un fichier JSON.

    Le dossier parent du fichier est créé s'il n'existe pas.

    Args:
        statistiques: Données sérialisables à exporter.
        fichier: Chemin du fichier de sortie.

    Returns:
        Le chemin du fichier écrit, sous forme d'objet :class:`pathlib.Path`.
    """
    chemin = Path(fichier)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8") as fichier_sortie:
        json.dump(statistiques, fichier_sortie, indent=2, ensure_ascii=False)
    return chemin
