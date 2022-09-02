# read the contents of your README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="pychonet",
    author="Scott Phillips",
    author_email="scotty.phillips@hotmail.com",
    packages=["pychonet", "pychonet.lib"],
    url="http://pypi.python.org/pypi/pychonet/",
    license="LICENSE.txt",
    description="A library for interfacing via the ECHONETlite protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
