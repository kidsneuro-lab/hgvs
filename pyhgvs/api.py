from __future__ import print_function
from __future__ import unicode_literals

import os

from fastapi import FastAPI
from typing import Tuple,List
from pyfaidx import Fasta
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
import logging

logging.config.fileConfig('pyhgvs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

# Read genome sequence using pyfaidx.
file=os.getenv('FASTA')
if file is None:
    raise Exception(f"FASTA env var not set.")

logger.info('Loading FASTA: %s',file)
if not os.path.exists(file):
    raise Exception(f"FASTA file: {file} not found. Please check if file exists")

genome = Fasta(file)

# Read RefSeq transcripts into a python dict.

refgene=os.getenv('REFGENE')
if refgene is None:
    raise Exception(f"REFGENE env var not set.")

logger.info('Loading REFGENE: %s',refgene)
if not os.path.exists(refgene):
    raise Exception(f"REFGENE file: {refgene} not found. Please check if file exists")

with open(refgene) as infile:
    transcripts = hgvs_utils.read_transcripts(infile)

# Provide a callback for fetching a transcript by its name.
def get_transcript(name):
    return transcripts.get(name)

@app.get("/")
def get_root():
    return {"App": "HGVS Translator"}

@app.get("/health/alive")
def get_alive():
    return {"status": "alive"}

@app.get("/health/ready")
def get_ready():
    return {"status": "ready"}

@app.get("/translate", response_model=Tuple[str, int, str, str])
def translate_hgvs(value: str):
    logger.info('Translating %s', value)
    chrom, offset, ref, alt = hgvs.parse_hgvs_name(value, genome, get_transcript=get_transcript)
    logger.info('Translated %s to: %s %s %s %s', value, chrom, offset, ref, alt)
    return chrom, offset, ref, alt

@app.post("/translate_bulk")
def translate_hgvs_bulk(values: List[str]):
    translations = []
    logger.info('Translating %s values', {len(values)})
    for value in values:
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(value, genome, get_transcript=get_transcript)
        translations.append((value, chrom, offset, ref, alt))
    return translations

if __name__ == '__main__':
    app.run(debug=True)