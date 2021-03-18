import os

from .configloader import INIConfigLoader, TOMLConfigLoader

__version__ = open(os.path.join(".", "VERSION")).read().strip()
