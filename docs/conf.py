"""Configuration Sphinx pour la documentation du projet.

Génère une documentation HTML à partir des docstrings (style Google) des
paquets ``models``, ``core`` et ``out``.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Simulation de trafic routier"
author = "ING 3 - Python"
copyright = "2026, ING 3 - Python"
release = "1.0.0"
version = "1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_mock_imports = ["matplotlib"]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True

source_suffix = {
    ".rst": "restructuredtext",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "fr"
html_theme = "alabaster"
html_title = project
