# tests/test_process_entries.py
import tempfile
import difflib
from pathlib import Path
from pathlib import Path

import pytest

# Adjust this import to match your module name/location
from pyhgvs.scripts.hgvs import process_entries, InvalidHGVSName

@pytest.fixture
def genome():
    return "tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.Y.fa"

@pytest.fixture
def transcripts():
    return "tests/fixtures/genes.refGene"

def test_process_entries(genome, transcripts):
    input_file = "tests/fixtures/cli/input1.txt"
    output_expected_file = Path("tests/fixtures/cli/output1_expected.txt")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        output_file = tmp.name

    # Run the function under test
    process_entries(input_file, output_file, genome, transcripts, normalize=False)

    # Read both expected and actual output
    expected = output_expected_file.read_text().splitlines(keepends=True)
    actual = Path(output_file).read_text().splitlines(keepends=True)

    # If they differ, show a unified diff
    if expected != actual:
        diff = "".join(
            difflib.unified_diff(expected, actual, fromfile="expected", tofile="actual")
        )
        raise AssertionError(f"Output does not match expected:\n{diff}")

    # Otherwise test passes
    assert expected == actual
