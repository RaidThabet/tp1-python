"""Configuration pytest commune aux tests.

Ajoute la racine du projet au ``sys.path`` afin que les paquets ``models``,
``core`` et ``out`` soient importables quel que soit le répertoire courant.
"""

import sys
from pathlib import Path

RACINE_PROJET = Path(__file__).resolve().parents[1]
if str(RACINE_PROJET) not in sys.path:
    sys.path.insert(0, str(RACINE_PROJET))
