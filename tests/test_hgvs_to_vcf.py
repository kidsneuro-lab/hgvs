import logging
import csv
import os
import sys

import pytest
from pyfaidx import Fasta

current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder_path = os.path.join(current_dir, "..")
sys.path.append(target_folder_path)

import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
from pyhgvs.models.hgvs_name import InvalidHGVSName

logger = logging.getLogger(__name__)

def read_fixture_data(file_path: str, filter_expr = None) -> list[dict]:
    list_of_dicts = None
    with open(file_path, "r") as file:
        reader = csv.DictReader(file, delimiter="\t")
        list_of_dicts = list(reader)

    if filter_expr is not None:
        return list(filter(filter_expr, list_of_dicts))
    else:
        return list_of_dicts

class TestID:
    @staticmethod
    def idfn1(data: dict) -> str:
        return data['hgvs_c']
 
class TestHgvsToVCF:
    @pytest.fixture(scope="class")
    def genome(self):
        file=os.getenv('FASTA')
        logger.info(f"Loading fasta: {file}")

        if not os.path.exists(file):
            raise Exception(f"Fasta file: {file} not found. Please check if file exists or FASTA environment variable has been defined")

        genome = Fasta(file)
        yield genome

    @pytest.fixture(scope="class")
    def transcripts(self):
        refgene=os.getenv('REFGENE')
        logger.info(f"Refgene: {refgene}")

        if not os.path.exists(refgene):
            raise Exception(f"Refgene file: {refgene} not found. Please check if file exists or REFGENE environment variable has been defined")

        with open(refgene) as infile:
            transcripts = hgvs_utils.read_transcripts(infile)
        yield lambda name: transcripts.get(name)

    @pytest.mark.skip(reason="Requires FASTA assembly file to be present")   
    @pytest.mark.parametrize('hgvs_vcf_data', read_fixture_data("tests/fixtures/hgvs_vcf_valid.tsv"), ids=TestID.idfn1)
    def test_valid_hgvs(self, hgvs_vcf_data, genome: Fasta, transcripts):
        chr, pos, ref, alt = hgvs.parse_hgvs_name(hgvs_name=hgvs_vcf_data['hgvs_c'], genome=genome, get_transcript=transcripts, lazy=True)

        scenario_1 = (chr == hgvs_vcf_data['chr']) and (pos == int(hgvs_vcf_data['pos'])) and (ref == hgvs_vcf_data['ref']) and (alt == hgvs_vcf_data['alt'])
        
        # The test data may not be left justified. This is to check for those scenarios
        scenario_2 = (chr == hgvs_vcf_data['chr']) and (pos == int(hgvs_vcf_data['pos']) - 1) and (ref[1:] == hgvs_vcf_data['ref']) and (alt[1:] == hgvs_vcf_data['alt'])

        assert scenario_1 or scenario_2

    @pytest.mark.skip(reason="Requires FASTA assembly file to be present")   
    @pytest.mark.parametrize('hgvs_vcf_data', read_fixture_data("tests/fixtures/hgvs_vcf_invalid.tsv"), ids=TestID.idfn1)
    def test_invalid_hgvs(self, hgvs_vcf_data, genome: Fasta, transcripts):
        with pytest.raises(InvalidHGVSName):
            hgvs.parse_hgvs_name(hgvs_name=hgvs_vcf_data['hgvs_c'], genome=genome, get_transcript=transcripts, lazy=True)