"""
Non-coding DNA HGVS parser (n. prefix).

Handles parsing of non-coding DNA HGVS names like NR_123456.1:n.123A>T
"""
from __future__ import annotations

from typing import Any, Dict

from .base import BaseHGVSParser
from ..models.hgvs_name import HGVSName
from .. import get_vcf_allele


class NonCodingParser(BaseHGVSParser):
    """Parser for non-coding DNA HGVS names (n. prefix)."""
    
    @property
    def supported_prefix(self) -> str:
        """Return the supported HGVS prefix."""
        return 'n.'
    
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse non-coding DNA HGVS name structure.
        
        Args:
            hgvs_name: The non-coding DNA HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        return HGVSName(hgvs_name)
    
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from non-coding DNA HGVS name.
        
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