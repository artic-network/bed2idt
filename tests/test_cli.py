from typer.testing import CliRunner

import pathlib

from bed2idt.main import app
from bed2idt.__init__ import __version__

runner = CliRunner()

# This uses pytest rather than unittest
# Run using: poetry run pytest

BEDFILE_INPUT = pathlib.Path("tests/test_input/primer.bed")
EXISTING_OUTPUT = pathlib.Path("tests/test_output/output.xlsx")


# Test the app can run
def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0


# Test the app can run with the version flag
def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_plate_generate():

    result = runner.invoke(
        app,
        [
            "plates",
            "--output",
            str(EXISTING_OUTPUT.absolute()),
            str(BEDFILE_INPUT.absolute()),
        ],
    )
    assert result.exit_code == 2  # Should error as the output file already exists
