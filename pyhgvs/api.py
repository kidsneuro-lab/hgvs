from __future__ import print_function
from __future__ import unicode_literals

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from typing import Tuple,List
from pyfaidx import Fasta
import pyhgvs as hgvs
from pyhgvs.models.hgvs_name import InvalidHGVSName
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

@app.post("/translate", response_model=Tuple[str, int, str, str])
async def translate_hgvs(request: Request):
    data = await request.json()
    value = data.get("value")
    logger.info('Translating %s', value)
    try:
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(value, genome, get_transcript=get_transcript)
        logger.info('Translated %s to: %s %s %s %s', value, chrom, offset, ref, alt)
        return chrom, offset, ref, alt
    except InvalidHGVSName:
        error_message = f"Invalid HGVS Name:'{value}'"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    except ValueError as e:
        error_message = str(e)
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/translate_bulk")
def translate_hgvs_bulk(values: List[str]):
    translations = []
    logger.info('Translating %s values', {len(values)})
    try:
        for value in values:
            chrom, offset, ref, alt = hgvs.parse_hgvs_name(value, genome, get_transcript=get_transcript)
            translations.append((value, chrom, offset, ref, alt))
        return translations
    except InvalidHGVSName:
        error_message = f"Invalid HGVS Name:'{value}'"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    except ValueError as e:
        error_message = str(e)
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    
if __name__ == '__main__':
    app.run(debug=True)