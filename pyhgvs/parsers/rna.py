"""
RNA HGVS parser (r. prefix).

Handles parsing of RNA HGVS names like NM_123456.1:r.123a>u
"""
from __future__ import annotations

from typing import Any, Dict

from .base import BaseHGVSParser
from ..models.hgvs_name import HGVSName
from .. import get_vcf_allele


class RNAParser(BaseHGVSParser):
    """Parser for RNA HGVS names (r. prefix)."""
    
    @property
    def supported_prefix(self) -> str:
        """Return the supported HGVS prefix."""
        return 'r.'
    
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse RNA HGVS name structure.
        
        Args:
            hgvs_name: The RNA HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        return HGVSName(hgvs_name)
    
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from RNA HGVS name.
        
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