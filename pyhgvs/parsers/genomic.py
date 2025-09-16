"""
Genomic HGVS parser (g. prefix).

Handles parsing of genomic HGVS names like NC_000001.11:g.123456A>T
"""
from __future__ import annotations

from typing import Any, Dict

from .base import BaseHGVSParser
from ..models.hgvs_name import HGVSName
from .. import get_vcf_allele


class GenomicParser(BaseHGVSParser):
    """Parser for genomic HGVS names (g. prefix)."""
    
    @property
    def supported_prefix(self) -> str:
        """Return the supported HGVS prefix."""
        return 'g.'
    
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse genomic HGVS name structure.
        
        Args:
            hgvs_name: The genomic HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        return HGVSName(hgvs_name)
    
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from genomic HGVS name.
        
        Args:
            hgvs: The parsed HGVS name
            
        Returns:
            Dictionary containing coordinate information
        """
        chrom, start, end, ref, alt = get_vcf_allele(hgvs, self.genome, self.transcript)
        
        return {
            'chrom': chrom,
            'pos': start,
            'ref': ref,
            'alt': alt,
            'start': start,
            'end': end
        }