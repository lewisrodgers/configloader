import os

from .config import INIConfigLoader, TOMLConfigLoader

__version__ = open(os.path.join(".", "VERSION")).read().strip()
