#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from contextlib import contextmanager

from setuptools import find_packages, setup

# Package meta-data.
NAME = "readabilipy"
DESCRIPTION = "Python wrapper for Mozilla's Readability.js"
URL = "https://github.com/alan-turing-institute/ReadabiliPy"
AUTHOR = "The Alan Turing Institute"
AUTHOR_EMAIL = "info@turing.ac.uk"
MAINTAINER = "James Robinson"
MAINTAINER_EMAIL = "jrobinson@turing.ac.uk"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "beautifulsoup4>=4.7.1",
    "html5lib",
    "lxml",
    "regex",
]

docs_require = ["sphinx", "m2r"]
test_require = ["coveralls", "pycodestyle", "pyflakes", "pylint", "pytest", "pytest-benchmark", "pytest-cov"]
dev_require = []

# What packages are optional?
EXTRAS = {
    "docs": docs_require,
    "test": test_require,
    "dev": docs_require + test_require + dev_require,
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


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    entry_points={
        "console_scripts": ["readabilipy=readabilipy.__main__:main"],
    },
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
