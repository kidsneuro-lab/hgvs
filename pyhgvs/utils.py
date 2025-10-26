"""
Helper functions for HGVS processing.
"""
from __future__ import annotations

import operator
import os
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from .models.variants import Position
from .models.transcript import Transcript, CDNA_Match, Exon


def read_refgene(infile) -> Iterator[Dict[str, Any]]:
    """
    Read RefGene format file.
    
    RefGene = genePred with extra column at front (and ignored ones after)
    
    Args:
        infile: File handle to read from
        
    Yields:
        Dictionary containing gene/transcript information
    """
    return read_genepred(infile, skip_first_column=True)


def read_genepred(infile, skip_first_column: bool = False) -> Iterator[Dict[str, Any]]:
    """
    Read GenePred extension format file.
    
    GenePred extension format:
    http://genome.ucsc.edu/FAQ/FAQformat.html#GenePredExt

    Column definitions:
    0. string name;                 "Name of gene (usually transcript_id from GTF)"
    1. string chrom;                "Chromosome name"
    2. char[1] strand;              "+ or - for strand"
    3. uint txStart;                "Transcription start position"
    4. uint txEnd;                  "Transcription end position"
    5. uint cdsStart;               "Coding region start"
    6. uint cdsEnd;                 "Coding region end"
    7. uint exonCount;              "Number of exons"
    8. uint[exonCount] exonStarts;  "Exon start positions"
    9. uint[exonCount] exonEnds;    "Exon end positions"
    10. uint id;                    "Unique identifier"
    11. string name2;               "Alternate name (e.g. gene_id from GTF)"
    
    Args:
        infile: File handle to read from
        skip_first_column: Whether to skip the first column
        
    Yields:
        Dictionary containing transcript information
    """
    for line in infile:
        # Skip comments.
        if line.startswith('#'):
            continue
        row = line.rstrip('\n').split('\t')
        if skip_first_column:
            row = row[1:]

        # Skip trailing ,
        exon_starts = list(map(int, row[8].split(',')[:-1]))
        exon_ends = list(map(int, row[9].split(',')[:-1]))
        exons = list(zip(exon_starts, exon_ends))

        yield {
            'chrom': row[1],
            'start': int(row[3]),
            'end': int(row[4]),
            'id': row[0],
            'strand': row[2],
            'cds_start': int(row[5]),
            'cds_end': int(row[6]),
            'gene_name': row[11],
            'exons': exons,
        }


def make_transcript(transcript_json):
    """
    Make a Transcript form a JSON object.
    """

    transcript_name = transcript_json['id']
    if '.' in transcript_name:
        name, version = transcript_name.split('.')
    else:
        name, version = transcript_name, None

    transcript = Transcript(
        name=name,
        version=int(version) if version is not None else None,
        gene=transcript_json['gene_name'],
        tx_position=Position(
            transcript_json['chrom'],
            transcript_json['start'],
            transcript_json['end'],
            transcript_json['strand'] == '+'),
        cds_position=Position(
            transcript_json['chrom'],
            transcript_json['cds_start'],
            transcript_json['cds_end'],
            transcript_json['strand'] == '+'),
        start_codon_transcript_pos=transcript_json.get("start_codon_transcript_pos"),
        stop_codon_transcript_pos=transcript_json.get("stop_codon_transcript_pos"),
    )

    exons = transcript_json['exons']
    exons.sort(key=operator.itemgetter(0))
    cdna_match = transcript_json.get('cdna_match', [])
    cdna_match.sort(key=operator.itemgetter(0))

    if not transcript.tx_position.is_forward_strand:
        exons.reverse()
        cdna_match.reverse()

    # We don't use exons, but run everything through cDNA match so there's just 1 path
    # exons are treated as a perfect cDNA match
    if not cdna_match:
        cdna_match = json_perfect_exons_to_cdna_match(exons)

    for number, (exon_start, exon_end, cdna_start, cdna_end, gap) in enumerate(cdna_match, 1):
        transcript.cdna_match.append(CDNA_Match(transcript=transcript,
                                                tx_position=Position(
                                                    transcript_json['chrom'],
                                                    exon_start,
                                                    exon_end,
                                                    transcript_json['strand'] == '+'),
                                                cdna_start=cdna_start,
                                                cdna_end=cdna_end,
                                                gap=gap,
                                                number=number))

    return transcript


def json_perfect_exons_to_cdna_match(ordered_exons, single=False):
    """ Perfectly matched exons are basically a no-gap case of cDNA match
        single - use a single cDNA match (deletions for introns) - this is currently broken do not use
    """
    cdna_match = []
    if single:
        ordered_exons = list(ordered_exons)
        start = ordered_exons[0][0]
        end = ordered_exons[-1][1]
        last_exon_end = None
        gap_list = []
        cdna_length = 0
        for (exon_start, exon_end) in ordered_exons:
            # end up looking like "M D M D (M=exon, D=intron length)"
            if last_exon_end:
                intron_length = abs(exon_start - last_exon_end)
                gap_list.append("D%d" % intron_length)
            exon_length = exon_end - exon_start
            cdna_length += exon_length
            gap_list.append("M%d" % exon_length)
            last_exon_end = exon_end
        cdna_match = [[start, end, 1, cdna_length, " ".join(gap_list)]]
    else:
        cdna_start = 1
        for (exon_start, exon_end) in ordered_exons:
            exon_length = exon_end - exon_start
            cdna_end = cdna_start + exon_length - 1
            cdna_match.append([exon_start, exon_end, cdna_start, cdna_end, None])
            cdna_start = cdna_end + 1
    return cdna_match


def read_transcripts(refgene_file):
    """
    Read all transcripts in a RefGene file.
    """
    transcripts = {}
    for trans in (make_transcript(record)
                  for record in read_refgene(refgene_file)):   

        if trans.name not in transcripts.keys():
            transcripts[trans.name] = {}
            transcripts[trans.full_name] = {}

        if trans.tx_position.chrom not in transcripts[trans.name].keys():
            transcripts[trans.name][trans.tx_position.chrom] = trans
            transcripts[trans.full_name][trans.tx_position.chrom] = trans        

    return transcripts

class TranscriptProvider:
    """
    Provider for transcript information with improved error handling and validation.
    
    This class encapsulates transcript data loading and retrieval,
    providing a clean interface for accessing transcript information.
    """
    
    def __init__(self, refgene_file: Optional[str] = None, env_var: str = "REFGENE") -> None:
        """
        Initialize TranscriptProvider.

        Args:
            refgene_file: Path to the file. If None, will try environment variable.
            env_var: Name of the environment variable to check if refgene_file is not given.
            
        Raises:
            ValueError: If no file path is provided and environment variable is not set
            FileNotFoundError: If the specified file does not exist
        """
        # Try direct path first
        if refgene_file is not None:
            self._refgene_file = refgene_file
        else:
            # Fallback to environment variable
            env_path = os.getenv(env_var)
            if env_path is None:
                raise ValueError(f"No file path provided and environment variable '{env_var}' is not set.")
            self._refgene_file = env_path

        # Check file existence
        if not Path(self._refgene_file).exists():
            raise FileNotFoundError(f"File not found: {self._refgene_file}")

        # Load the file
        self._transcripts = self._load_file()

    def _load_file(self) -> Dict[str, Dict[str, Transcript]]:
        """
        Load the file contents.
        
        Returns:
            Dictionary mapping transcript names to chromosome-specific transcripts
            
        Raises:
            IOError: If file cannot be read
            ValueError: If file format is invalid
        """
        try:
            with open(self._refgene_file) as infile:
                return read_transcripts(infile)
        except IOError as e:
            raise IOError(f"Failed to read transcript file '{self._refgene_file}': {e}")
        except Exception as e:
            raise ValueError(f"Invalid file format in '{self._refgene_file}': {e}")

    def _get_transcript(self, name: str) -> Optional[Transcript]:
        """
        Provide a callback for fetching a transcript by its name.
        
        Args:
            name: Transcript name
            
        Returns:
            Transcript object if found, None otherwise
            
        Raises:
            RuntimeError: If multiple loci are found for the transcript
        """
        if not name:
            return None
            
        tx = self._transcripts.get(name)

        if tx is not None:
            if len(tx) != 1:
                raise RuntimeError(f"Multiple loci: {', '.join(list(tx.keys()))} found for transcript: {name}")
            
            return tx[next(iter(tx))]
        else:
            return None

    def _get_transcript_X_over_Y(self, name: str) -> Optional[Transcript]:
        """
        Provide a callback for fetching a transcript by its name, prioritizing X over Y.
        
        Args:
            name: Transcript name
            
        Returns:
            Transcript object if found, None otherwise
            
        Raises:
            RuntimeError: If multiple loci are found for the transcript (excluding X/Y case)
        """
        if not name:
            return None
            
        tx = self._transcripts.get(name)

        if tx is not None:
            # Check if both keys 'X' and 'Y' are in the dictionary
            if 'X' in tx and 'Y' in tx:
                return tx['X']

            if len(tx) != 1:
                raise RuntimeError(f"Multiple loci: {', '.join(list(tx.keys()))} found for transcript: {name}")
            
            return tx[next(iter(tx))]
        else:
            return None

    def get_transcripts_fn(self, prioritise_X_over_Y: bool = False) -> Callable[[str], Optional[Transcript]]:
        """
        Get a transcript retrieval function with specified behavior.
        
        Args:
            prioritise_X_over_Y: Whether to prioritize X chromosome over Y for paralogous genes
            
        Returns:
            Function that takes a transcript name and returns a Transcript or None
        """
        if prioritise_X_over_Y:
            return self._get_transcript_X_over_Y
        else:
            return self._get_transcript
    
    def get_transcript_count(self) -> int:
        """
        Get the total number of transcripts loaded.
        
        Returns:
            Number of transcripts
        """
        return len(self._transcripts)
    
    def get_available_transcripts(self) -> List[str]:
        """
        Get list of available transcript names.
        
        Returns:
            List of transcript names
        """
        return list(self._transcripts.keys())