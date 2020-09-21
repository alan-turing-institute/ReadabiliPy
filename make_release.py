#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Do-nothing script for making a release

This idea comes from here:
https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/

This file is part of ReadabiliPy.

Copyright: 2020, The Alan Turing Institute
License: See LICENSE file.

"""

import os
import sys
import tempfile
import webbrowser

try:
    import colorama
    colorama.init()
    BE_COLOURFUL = True
except ImportError:
    BE_COLOURFUL = False


URLS = {
    # "RTD": "https://readthedocs.org/projects/readabilipy/builds/",
    "Travis": "https://travis-ci.org/alan-turing-institute/ReadabiliPy",
}


def coloured(msg, colour=None, style=None):
    if not BE_COLOURFUL:
        return msg

    colours = {
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "cyan": colorama.Fore.CYAN,
        "yellow": colorama.Fore.YELLOW,
        "magenta": colorama.Fore.MAGENTA,
        None: "",
    }
    styles = {
        "bright": colorama.Style.BRIGHT,
        "dim": colorama.Style.DIM,
        None: "",
    }
    pre = colours[colour] + styles[style]
    post = colorama.Style.RESET_ALL
    return f"{pre}{msg}{post}"


def cprint(msg, colour=None, style=None):
    print(coloured(msg, colour=colour, style=style))


def wait_for_enter():
    input(coloured("\nPress Enter to continue", style="dim"))
    print()


def get_package_name():
    with open("./setup.py", "r") as fp:
        nameline = next(
            (line.strip() for line in fp if line.startswith("NAME = ")), None
        )
        return nameline.split("=")[-1].strip().strip('"')


def get_package_version(pkgname):
    ctx = {}
    with open(f"{pkgname.lower()}/__version__.py", "r") as fp:
        exec(fp.read(), ctx)
    return ctx["__version__"]


class Step:
    def pre(self, context):
        pass

    def post(self, context):
        wait_for_enter()

    def run(self, context):
        try:
            self.pre(context)
            self.action(context)
            self.post(context)
        except KeyboardInterrupt:
            cprint("\nInterrupted.", colour="red")
            raise SystemExit(1)

    def instruct(self, msg):
        cprint(msg, colour="green")

    def print_run(self, msg):
        cprint("Run:", colour="cyan", style="bright")
        self.print_cmd(msg)

    def print_cmd(self, msg):
        cprint("\t" + msg, colour="cyan", style="bright")

    def do_cmd(self, cmd):
        cprint(f"Going to run: {cmd}", colour="magenta", style="bright")
        wait_for_enter()
        os.system(cmd)


class GitToMaster(Step):
    def action(self, context):
        self.instruct("Make sure you're on master and changes are merged in")
        self.print_run("git checkout master")


class UpdateChangelog(Step):
    def action(self, context):
        self.instruct(f"Update change log for version {context['version']}")
        self.print_run("vi CHANGELOG.md")


class UpdateReadme(Step):
    def action(self, context):
        self.instruct("Update readme if necessary")
        self.print_run("vi README.md")


class RunTests(Step):
    def action(self, context):
        self.instruct("Run the unit tests")
        self.print_run("make test")


class BumpVersionPackage(Step):
    def action(self, context):
        self.instruct("Update __version__.py with the new version")

    def post(self, context):
        wait_for_enter()
        context["version"] = self._get_version(context)

    def _get_version(self, context):
        # Get the version from the version file
        return get_package_version(context["pkgname"])


class MakeClean(Step):
    def action(self, context):
        self.do_cmd("make clean")


class MakeDocs(Step):
    def action(self, context):
        self.do_cmd("make docs")


class MakeDist(Step):
    def action(self, context):
        self.do_cmd("make dist")


class PushToTestPyPI(Step):
    def action(self, context):
        self.do_cmd(
            "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
        )


class InstallFromTestPyPI(Step):
    def action(self, context):
        tmpvenv = tempfile.mkdtemp(prefix="rdpy_venv_")
        self.do_cmd(
            f"python -m venv {tmpvenv} && source {tmpvenv}/bin/activate && "
            "pip install --no-cache-dir --index-url "
            "https://test.pypi.org/simple/ "
            "--extra-index-url https://pypi.org/simple "
            f"{context['pkgname']}=={context['version']}"
        )
        context["tmpvenv"] = tmpvenv


class TestPackage(Step):
    def action(self, context):
        self.instruct(
            f"Ensure that the following command gives version {context['version']}"
        )
        self.do_cmd(f"source {context['tmpvenv']}/bin/activate && readabilipy -V")


class RemoveVenv(Step):
    def action(self, context):
        self.do_cmd(f"rm -rf {context['tmpvenv']}")


class GitTagVersion(Step):
    def action(self, context):
        self.do_cmd(f"git tag v{context['version']}")


class GitAdd(Step):
    def action(self, context):
        self.instruct("Add everything to git and commit")
        self.print_run("git gui")


class PushToPyPI(Step):
    def action(self, context):
        self.do_cmd("twine upload dist/*")


class PushToGitHub(Step):
    def action(self, context):
        self.do_cmd("git push -u --tags origin master")


class WaitForTravis(Step):
    def action(self, context):
        webbrowser.open(URLS['Travis'])
        self.instruct(
            "Wait for Travis to complete and verify that its successful"
        )


class WaitForRTD(Step):
    def action(self, context):
        self.instruct(
            "Wait for ReadTheDocs to complete and verify that its successful"
        )


def main(target=None):
    procedure = [
        ("gittomaster", GitToMaster()),
        ("clean1", MakeClean()),
        ("tests1", RunTests()),
        ("gitadd1", GitAdd()),
        ("push1", PushToGitHub()),
        ("travis1", WaitForTravis()),
        ("bumpversion", BumpVersionPackage()),
        ("changelog", UpdateChangelog()),
        ("readme", UpdateReadme()),
        # ("docs", MakeDocs()),
        ("dist", MakeDist()),
        ("testpypi", PushToTestPyPI()),
        ("install", InstallFromTestPyPI()),
        ("testpkg", TestPackage()),
        ("remove_venv", RemoveVenv()),
        ("gitadd2", GitAdd()),
        ("pypi", PushToPyPI()),
        ("tag", GitTagVersion()),
        ("push2", PushToGitHub()),
    ]
    context = {}
    context["pkgname"] = get_package_name()
    context["version"] = get_package_version(context["pkgname"])
    skip = True if target else False
    for name, step in procedure:
        if not name == target and skip:
            continue
        skip = False
        step.run(context)
    cprint("\nDone!", colour="yellow", style="bright")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target=target)
