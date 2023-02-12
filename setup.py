import os
from setuptools import setup


def read(fname):
    """Simple function to read and return a file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ANCLab",
    version="0.0.1",
    author="Sajil C. K.",
    author_email="sajilck@gmail.com",
    description=("A Python package for simulating\
        Active Noise Control (ANC) experiments."),
    url="http://packages.python.org/anclab",
    packages=['anclab', 'tests'],
    long_description=read('README')
)
