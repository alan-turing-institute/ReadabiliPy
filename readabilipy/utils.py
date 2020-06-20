# -*- coding: utf-8 -*-

"""Utility functions

"""

import os

from contextlib import contextmanager


@contextmanager
def chdir(path):
    """Change directory in context and return to original on exit"""
    # From https://stackoverflow.com/a/37996581, couldn't find a built-in
    original_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_path)
