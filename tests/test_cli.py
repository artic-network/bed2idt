import pathlib

from typer.testing import CliRunner

from bed2idt.__init__ import __version__
from bed2idt.main import app

runner = CliRunner()

# This uses pytest rather than unittest
# Run using: poetry run pytest

BEDFILE_INPUT = pathlib.Path("tests/test_input/primer.bed")
EXISTING_OUTPUT = pathlib.Path("tests/test_output/output.xlsx")
NON_EXISTING_OUTPUT = pathlib.Path("tests/test_output/output2.xlsx")

# Ensure NON_EXISTING_OUTPUT does not exist
if NON_EXISTING_OUTPUT.exists():
    NON_EXISTING_OUTPUT.unlink()


# Test the app can run
def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0


# Test the app can run with the version flag
def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_plate_generate_exists():
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


def test_plate_generate_okay():
    result = runner.invoke(
        app,
        [
            "plates",
            "--output",
            str(NON_EXISTING_OUTPUT.absolute()),
            str(BEDFILE_INPUT.absolute()),
        ],
    )
    assert result.exit_code == 0  # Be okay as the output file does not exist
    assert NON_EXISTING_OUTPUT.exists()  # Check the output file was created

    # Clean up the output file
    NON_EXISTING_OUTPUT.unlink()
