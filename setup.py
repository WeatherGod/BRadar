import os
from setuptools import setup

setup(
    name = "BRadar",
    version = "0.5.0",
    author = "Benjamin Root",
    author_email = "ben.v.root@gmail.com",
    description = "Utilities for processing and displaying radar data.",
    license = "BSD",
    keywords = "radar",
    url = "https://github.com/WeatherGod/BRadar",
    packages = ['BRadar',],
    package_dir = {'': 'lib'},
    package_data = {'BRadar': ['shapefiles/countyp020.*', 'shapefiles/road_l.*']}

    )

