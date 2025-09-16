"""
Coding DNA HGVS parser (c. prefix).

Handles parsing of coding DNA HGVS names like NM_123456.1:c.123A>T
"""
from __future__ import annotations

from typing import Any, Dict

from .base import BaseHGVSParser
from ..models.hgvs_name import HGVSName
from .. import get_vcf_allele


class CodingParser(BaseHGVSParser):
    """Parser for coding DNA HGVS names (c. prefix)."""
    
    @property
    def supported_prefix(self) -> str:
        """Return the supported HGVS prefix."""
        return 'c.'
    
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse coding DNA HGVS name structure.
        
        Args:
            hgvs_name: The coding DNA HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        return HGVSName(hgvs_name)
    
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from coding DNA HGVS name.
        
        Args:
            hgvs: The parsed HGVS name
            
        Returns:
            Dictionary containing coordinate information
        """
        if not self.transcript:
            raise ValueError("Transcript is required for coding DNA variants")
            
        chrom, start, end, ref, alt = get_vcf_allele(hgvs, self.genome, self.transcript)
        
        return {
            'chrom': chrom,
            'pos': start,
            'ref': ref,
            'alt': alt,
            'start': start,
            'end': end
        }