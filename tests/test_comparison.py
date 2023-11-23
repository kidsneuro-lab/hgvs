import csv
import os
import sys
import pytest
import logging

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder_path = os.path.join(current_dir, "..")
sys.path.append(target_folder_path)

def read_csv(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader = csv.DictReader(csvfile)
        next(reader)  # Skip the header row
        return list(reader)

ensembl_csv_data = read_csv('tests/fixtures/downloads/output_ensemble.csv')
variant_validator_csv_data = read_csv('tests/fixtures/downloads/output_variant_validator.csv')

@pytest.mark.parametrize("row", ensembl_csv_data)
def test_against_ensembl(row):
    logger.info(f"Using row: {row}")
    hgvs = row['HGVS']
    success = row['Success'] == "True"
    chromosome = row['Chromosome']
    position = row['Position']
    reference = row['Ref']
    alternate = row['Alt']
    assert chromosome == "X", f"The chromosome should be X"

@pytest.mark.parametrize("row", variant_validator_csv_data)
def test_against_variant_validator(row):
    logger.info(f"Using row: {row}")
    hgvs = row['HGVS']
    success = row['Success'] == "True"
    chromosome = row['Chromosome']
    position = row['Position']
    reference = row['Ref']
    alternate = row['Alt']
    assert chromosome == "X", f"The chromosome should be X"
