"""
Factory for creating HGVS parsers.

This module implements the Factory pattern to create appropriate
HGVS parsers based on the HGVS type.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Type

from .base import BaseHGVSParser
from .genomic import GenomicParser
from .coding import CodingParser
from .noncoding import NonCodingParser
from .rna import RNAParser
from .protein import ProteinParser


class HGVSParserFactory:
    """
    Factory for creating HGVS parsers.
    
    Uses the Factory pattern to create appropriate parsers based on
    the HGVS type prefix (g., c., n., r., p.).
    """
    
    _parsers: Dict[str, Type[BaseHGVSParser]] = {
        'g.': GenomicParser,
        'c.': CodingParser,
        'n.': NonCodingParser,
        'r.': RNAParser,
        'p.': ProteinParser,
    }
    
    @classmethod
    def create_parser(
        cls,
        hgvs_type: str,
        genome: Any,
        transcript: Optional[Any] = None
    ) -> BaseHGVSParser:
        """
        Create an appropriate HGVS parser.
        
        Args:
            hgvs_type: The HGVS type prefix (e.g., 'g.', 'c.')
            genome: Genome sequence data
            transcript: Optional transcript information
            
        Returns:
            Appropriate parser instance
            
        Raises:
            ValueError: If the HGVS type is not supported
        """
        if hgvs_type not in cls._parsers:
            raise ValueError(
                f"Unsupported HGVS type: {hgvs_type}. "
                f"Supported types: {list(cls._parsers.keys())}"
            )
        
        parser_class = cls._parsers[hgvs_type]
        return parser_class(genome, transcript)
    
    @classmethod
    def register_parser(cls, hgvs_type: str, parser_class: Type[BaseHGVSParser]) -> None:
        """
        Register a new parser type.
        
        This allows extending the factory with custom parsers.
        
        Args:
            hgvs_type: The HGVS type prefix
            parser_class: The parser class to register
        """
        cls._parsers[hgvs_type] = parser_class
    
    @classmethod
    def get_supported_types(cls) -> list[str]:
        """
        Get list of supported HGVS types.
        
        Returns:
            List of supported HGVS type prefixes
        """
        return list(cls._parsers.keys())
    
    @classmethod
    def detect_hgvs_type(cls, hgvs_name: str) -> str:
        """
        Detect the HGVS type from a name.
        
        Args:
            hgvs_name: The HGVS name to analyze
            
        Returns:
            The detected HGVS type prefix
            
        Raises:
            ValueError: If the HGVS type cannot be detected
        """
        # Simple detection based on prefix
        for hgvs_type in cls._parsers.keys():
            if hgvs_type in hgvs_name:
                return hgvs_type
        
        raise ValueError(f"Cannot detect HGVS type from: {hgvs_name}")
    
    @classmethod
    def create_parser_auto(
        cls,
        hgvs_name: str,
        genome: Any,
        transcript: Optional[Any] = None
    ) -> BaseHGVSParser:
        """
        Create parser by auto-detecting HGVS type.
        
        Args:
            hgvs_name: The HGVS name to parse
            genome: Genome sequence data
            transcript: Optional transcript information
            
        Returns:
            Appropriate parser instance
        """
        hgvs_type = cls.detect_hgvs_type(hgvs_name)
        return cls.create_parser(hgvs_type, genome, transcript)