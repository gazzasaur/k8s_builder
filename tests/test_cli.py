import pytest

from k8s_builder.cli import main

__author__ = "gazzasaur"
__copyright__ = "gazzasaur"
__license__ = "MIT"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-f", "myfile.json"])
    captured = capsys.readouterr()
    assert "" in captured.out
