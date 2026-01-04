# src/coherex/__init__.py
# src/coherex/__init__.py
# Example exports of core components
from .core.metaphysics import MetaphysicalEngine
from .core.condensation_pipeline import CondensationPipeline
from .cli import main as cli_main # If cli.py provides a main entry point
__version__ = "0.1.0"
# Optional: Define what gets imported with 'from coherex import *'
__all__ = [
    "MetaphysicalEngine",
    "CondensationPipeline",
    "cli_main",
    # Add other top-level exports here
]