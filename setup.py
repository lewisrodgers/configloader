import os

from setuptools import setup

with open(os.path.join(".", "VERSION")) as version_file:
    version = version_file.read().strip()

setup(
    name="configloader",
    version=version,
    description="Configuration loader",
    author="Lewis Rodgers",
    author_email="lrodgers04@gmail.com",
    packages=["configloader"]
)
