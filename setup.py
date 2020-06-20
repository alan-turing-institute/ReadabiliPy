#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import subprocess
import sys

from contextlib import contextmanager

from setuptools import find_packages, setup
from setuptools.command.install import install

# Package meta-data.
NAME = "readabilipy"
DESCRIPTION = "Python wrapper for Mozilla's Readability.js"
URL = "https://github.com/alan-turing-institute/ReadabiliPy"
EMAIL = "jrobinson@turing.ac.uk"
AUTHOR = "The Alan Turing Institute"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"

# What packages are required for this module to be executed?
REQUIRED = [
    "beautifulsoup4>=4.7.1",
    "html5lib",
    "lxml",
    "regex",
]

# What packages are optional?
EXTRAS = {
    "dev": [
        "pycodestyle",
        "pyflakes",
        "pylint",
        "pytest",
        "pytest-benchmark",
        "pytest-cov",
        "python-coveralls",
    ]
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


@contextmanager
def chdir(path):
    # From https://stackoverflow.com/a/37996581, couldn't find a built-in
    original_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_path)


class CustomInstall(install):
    def have_npm(self):
        cp = subprocess.run(
            ["npm", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return cp.returncode == 0

    def have_package_json(self):
        pkgjson = os.path.join(here, "package.json")
        return os.path.exists(pkgjson)

    def run(self):
        # run original install code
        install.run(self)

        # Run NPM installation
        if not self.have_npm():
            print(
                "Warning: NPM is needed to use Readability.js.",
                file=sys.stderr,
            )
            return

        if not self.have_package_json():
            print(
                "Error: Couldn't find package.json. This is unexpected.",
                file=sys.stderr,
            )
            return

        jsdir = os.path.join(self.install_lib, NAME, "javascript")
        with chdir(jsdir):
            subprocess.check_call(["npm", "install"])


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    entry_points={
        "console_scripts": ["readabilipy=readabilipy.__main__:main"],
    },
    cmdclass={"install": CustomInstall},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)