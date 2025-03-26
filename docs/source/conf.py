# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ILW'
copyright = '2025, Vojtěch Mrkos'
author = 'Vojtěch Mrkos'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme' 
# Add these extensions
extensions = [
    'sphinx.ext.autodoc',  # Core extension for auto-documenting modules
    'sphinx.ext.viewcode',  # Add links to highlighted source code
    'sphinx.ext.napoleon',  # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',  # Link to other project's documentation
    'sphinx.ext.coverage',  # Check document coverage
    'sphinx.ext.autosummary',  # Generate summary tables
    "sphinxcontrib.autodoc_pydantic"
]

# Optional: Use a nice theme

# Add your project's Python path if needed
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Adjust this path to point to your module directory

# Napoleon settings (if you're using Google or NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Generate documentation for all members, including private ones if desired
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    # 'private-members': True,  # Uncomment if you want to include private members
}

# Autosummary settings
autosummary_generate = True
