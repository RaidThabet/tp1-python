"""Point d'entrée de la simulation de trafic.

Lance une simulation de 120 tours sur le réseau par défaut puis affiche les
statistiques finales et le graphique associé.
"""

from core.simulateur import Simulateur
from out.affichage import afficher_statistiques

simu = Simulateur()
resultats = simu.lancer_simulation(n_tours=120, delta_t=1)
afficher_statistiques(resultats)
