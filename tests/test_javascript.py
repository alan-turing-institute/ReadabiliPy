import subprocess
import sys

import pytest

from checks import check_extract_article
from readabilipy import simple_json, utils


def test_extract_simple_article_with_readability_js():
    check_extract_article(
        "plain-content-test_full_article.html",
        "plain-content-test_full_article_javascript.json",
        use_readability_js=True
    )


def test_extract_article_from_page_with_readability_js():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_full_page_javascript.json",
        use_readability_js=True
    )


def test_npm_install_keeps_diagnostics_off_stdout(tmp_path, monkeypatch, capfd):
    jsdir = tmp_path / "javascript"
    jsdir.mkdir()
    (jsdir / "package.json").write_text("{}")
    monkeypatch.setattr(utils, "__file__", str(tmp_path / "utils.py"))
    monkeypatch.setattr(utils, "have_npm", lambda: True)
    run = subprocess.run

    def install_output(_command, check, **kwargs):
        return run([sys.executable, "-c", "print('install diagnostic')"], check=check, **kwargs)

    monkeypatch.setattr(utils.subprocess, "run", install_output)
    utils.run_npm_install()
    captured = capfd.readouterr()
    assert captured.out == ""
    assert captured.err == "install diagnostic\n"


def test_extraction_failure_keeps_diagnostics_off_stdout(tmp_path, monkeypatch, capfd):
    monkeypatch.setattr(simple_json, "have_node", lambda: True)
    monkeypatch.setattr(simple_json.tempfile, "tempdir", str(tmp_path))
    failure = subprocess.CalledProcessError(1, ["node"], stderr="extraction diagnostic")

    def fail_extraction(*_args, **_kwargs):
        raise failure

    monkeypatch.setattr(simple_json.subprocess, "run", fail_extraction)
    with pytest.raises(subprocess.CalledProcessError) as raised:
        simple_json.simple_json_from_html_string("<p>content</p>", use_readability=True)
    assert raised.value is failure
    captured = capfd.readouterr()
    assert captured.out == ""
    assert captured.err == "extraction diagnostic\n"
