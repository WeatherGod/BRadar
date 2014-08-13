from __future__ import print_function

import sys
import os
from setuptools import setup
try:
    from setuptools.command.build_py import build_py_2to3 as build_py
except ImportError:
    from setuptools.command.build_py import build_py

if sys.version_info[0] >= 3:
    def should_2to3(file, root):
        # Need to filter out files that may have already been made for py3k
        file = os.path.abspath(file)[len(os.path.abspath(root))+1:]
        return 'py3' not in file

    import multiprocessing
    def refactor(x):
        from lib2to3.refactor import RefactoringTool, get_fixers_from_package
        fixer_names = get_fixers_from_package('lib2to3.fixes')
        r = RefactoringTool(fixer_names, options=None)
        r.refactor([x], write=True)

    original_build_py = build_py
    class build_py(original_build_py):
        def run_2to3(self, files, *args):
            # We need to skip certain files that have already been
            # converted to Python 3.x
            filtered = [x for x in files if should_2to3(x, self.build_lib)]
            if sys.platform.startswith('win'):
                # doing this in parallel on windows may crash your computer
                apply(refactor, filtered)
            else:
                p = multiprocessing.Pool()
                for i, x in enumerate(p.imap_unordered(refactor, filtered)):
                    print("Running 2to3... %.02f%%" %
                          (float(i) / len(filtered) * 100.0), end='\r')
            print()


setup(
    name = "BRadar",
    version = "0.6.1",
    author = "Benjamin Root",
    author_email = "ben.v.root@gmail.com",
    description = "Utilities and scripts for processing and displaying"
                  " radar data.",
    license = "BSD",
    keywords = "radar",
    url = "https://github.com/WeatherGod/BRadar",
    packages = ['BRadar',],
    package_dir = {'': 'lib'},
    scripts = ['scripts/radarmovie.py',],
    package_data = {'BRadar': ['shapefiles/countyp020.*',
                               'shapefiles/road_l.*']},
    install_requires = ['numpy', 'scipy', 'matplotlib>=1.2', 'basemap',],
    cmdclass = {'build_py': build_py},
    )

