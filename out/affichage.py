"""Affichage et tracé graphique des statistiques de simulation."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def afficher_statistiques(statistiques):
    """Affiche un petit graphique Matplotlib des vitesses moyennes.

    Le graphique est enregistré sous ``statistiques.png`` à côté de ce module
    (backend ``Agg``, donc sans affichage interactif), puis un résumé textuel
    du dernier tour est imprimé sur la sortie standard.

    Args:
        statistiques: Liste de statistiques produite par
            :meth:`core.simulateur.Simulateur.lancer_simulation`. Si la liste
            est vide, un message est affiché et aucun graphique n'est créé.
    """
    if not statistiques:
        print("Aucune statistique disponible.")
        return

    tours = [s["tour"] for s in statistiques]
    vitesses = [s["vitesse_moyenne"] for s in statistiques]
    vitesses_min = [s.get("vitesse_min", s["vitesse_moyenne"]) for s in statistiques]
    vitesses_max = [s.get("vitesse_max", s["vitesse_moyenne"]) for s in statistiques]
    congestion = [s.get("routes_congestionnees", len(s["zones_congestion"])) for s in statistiques]
    vehicules_actifs = [s.get("vehicules_actifs", 0) for s in statistiques]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.fill_between(tours, vitesses_min, vitesses_max, color="tab:blue", alpha=0.18, label="Plage min/max")
    plt.plot(tours, vitesses, color="tab:blue", linewidth=2, label="Vitesse moyenne")
    plt.plot(tours, vitesses_min, color="tab:cyan", linestyle="--", linewidth=1, label="Vitesse min")
    plt.plot(tours, vitesses_max, color="tab:purple", linestyle="--", linewidth=1, label="Vitesse max")
    plt.title("Évolution des vitesses")
    plt.xlabel("Tour")
    plt.ylabel("km/h")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)

    ax_congestion = plt.subplot(1, 2, 2)
    ax_congestion.bar(tours, congestion, color="tab:red", alpha=0.75, label="Routes congestionnées")
    ax_congestion.set_title("Congestion et charge réseau")
    ax_congestion.set_xlabel("Tour")
    ax_congestion.set_ylabel("Routes congestionnées")
    ax_congestion.grid(True, axis="y", alpha=0.3)

    ax_charge = ax_congestion.twinx()
    ax_charge.plot(tours, vehicules_actifs, color="tab:green", linewidth=1.8, label="Véhicules actifs")
    ax_charge.set_ylabel("Véhicules actifs")

    handles_congestion, labels_congestion = ax_congestion.get_legend_handles_labels()
    handles_charge, labels_charge = ax_charge.get_legend_handles_labels()
    ax_congestion.legend(handles_congestion + handles_charge, labels_congestion + labels_charge, fontsize=8)

    plt.tight_layout()
    image_path = Path(__file__).resolve().parent / "statistiques.png"
    plt.savefig(image_path, dpi=150)
    plt.close()
    print(f"Graphique enregistré: {image_path}")

    dernier = statistiques[-1]
    print(f"Simulation terminée: {len(statistiques)} tours calculés.")
    print(f"Tour final: {dernier['tour']}, vitesse moyenne: {dernier['vitesse_moyenne']:.2f} km/h")
    print(f"Véhicules actifs: {dernier['vehicules_actifs']}")
    if dernier["zones_congestion"]:
        print("Zones de congestion:")
        for zone in dernier["zones_congestion"]:
            print(f"  - {zone['route']}: {zone['vitesse_moyenne']:.2f} km/h")
    else:
        print("Aucune zone de congestion détectée.")
