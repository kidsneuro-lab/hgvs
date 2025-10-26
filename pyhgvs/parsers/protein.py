"""
Protein HGVS parser (p. prefix).

Handles parsing of protein HGVS names like NP_123456.1:p.Lys123Asn
"""
from __future__ import annotations

from typing import Any, Dict

from .base import BaseHGVSParser
from ..models.hgvs_name import HGVSName


class ProteinParser(BaseHGVSParser):
    """Parser for protein HGVS names (p. prefix)."""
    
    @property
    def supported_prefix(self) -> str:
        """Return the supported HGVS prefix."""
        return 'p.'
    
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse protein HGVS name structure.
        
        Args:
            hgvs_name: The protein HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        return HGVSName(hgvs_name)
    
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from protein HGVS name.
        
        Note: Protein variants require special handling as they need
        to be converted back to genomic coordinates.
        
        Args:
            hgvs: The parsed HGVS name
            
        Returns:
            Dictionary containing coordinate information
        """
        # Protein parsing is more complex and may require
        # translation to genomic coordinates
        raise NotImplementedError(
            "Protein HGVS parsing is not yet implemented. "
            "This requires translation from protein to genomic coordinates."
        )