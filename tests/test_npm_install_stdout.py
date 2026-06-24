"""Regression test: run_npm_install must not leak npm output to stdout.

`npm install` prints progress/audit/funding lines to stdout. When ReadabiliPy is
imported by a program that communicates over stdout (e.g. an MCP stdio server),
that chatter corrupts the protocol stream. run_npm_install() must redirect stdout
to DEVNULL, matching the existing have_npm() precedent.
"""
import subprocess
from unittest import mock

from readabilipy import utils


def test_run_npm_install_suppresses_stdout():
    with mock.patch.object(utils, "have_npm", return_value=True), \
         mock.patch.object(utils.os.path, "exists", return_value=True), \
         mock.patch.object(utils.subprocess, "run") as run_mock:
        run_mock.return_value = mock.Mock(returncode=0)
        utils.run_npm_install()
        assert run_mock.called, "subprocess.run was not invoked"
        assert run_mock.call_args.kwargs.get("stdout") is subprocess.DEVNULL, (
            "npm install must pass stdout=subprocess.DEVNULL so it cannot "
            "corrupt stdout-based protocol consumers"
        )
