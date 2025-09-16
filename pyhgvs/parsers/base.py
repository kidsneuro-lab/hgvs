"""
Base HGVS parser using Template Method pattern.

This module defines the base structure and common workflow for all HGVS parsers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from ..models.hgvs_name import HGVSName


class BaseHGVSParser(ABC):
    """
    Base class for HGVS parsers implementing Template Method pattern.
    
    Defines the common workflow for parsing HGVS names while allowing
    subclasses to customize specific steps for different HGVS types.
    """
    
    def __init__(self, genome: Any, transcript: Optional[Any] = None) -> None:
        """
        Initialize the parser.
        
        Args:
            genome: Genome sequence data
            transcript: Optional transcript information
        """
        self.genome = genome
        self.transcript = transcript
    
    def parse(self, hgvs_name: str, **kwargs) -> Tuple[str, int, str, str]:
        """
        Template method for parsing HGVS names.
        
        This method defines the overall workflow:
        1. Validate input
        2. Parse the HGVS name
        3. Extract coordinates
        4. Normalize if requested
        5. Return standardized format
        
        Args:
            hgvs_name: The HGVS name to parse
            **kwargs: Additional parsing options
            
        Returns:
            Tuple of (chromosome, position, reference, alternative)
        """
        # Template method steps
        self._validate_input(hgvs_name)
        hgvs = self._parse_hgvs_structure(hgvs_name)
        coordinates = self._extract_coordinates(hgvs)
        
        if kwargs.get('normalize', True):
            coordinates = self._normalize_coordinates(coordinates)
            
        return self._format_output(coordinates)
    
    def _validate_input(self, hgvs_name: str) -> None:
        """
        Validate the input HGVS name.
        
        Args:
            hgvs_name: The HGVS name to validate
            
        Raises:
            ValueError: If the input is invalid
        """
        if not hgvs_name or not isinstance(hgvs_name, str):
            raise ValueError("HGVS name must be a non-empty string")
    
    @abstractmethod
    def _parse_hgvs_structure(self, hgvs_name: str) -> HGVSName:
        """
        Parse the HGVS name structure.
        
        This method is abstract and must be implemented by subclasses
        to handle the specific parsing logic for each HGVS type.
        
        Args:
            hgvs_name: The HGVS name to parse
            
        Returns:
            Parsed HGVSName object
        """
        pass
    
    @abstractmethod
    def _extract_coordinates(self, hgvs: HGVSName) -> Dict[str, Any]:
        """
        Extract coordinates from the parsed HGVS name.
        
        Args:
            hgvs: The parsed HGVS name
            
        Returns:
            Dictionary containing coordinate information
        """
        pass
    
    def _normalize_coordinates(self, coordinates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize coordinates according to standards.
        
        Default implementation does no normalization.
        Subclasses can override for specific normalization logic.
        
        Args:
            coordinates: Raw coordinate information
            
        Returns:
            Normalized coordinate information
        """
        return coordinates
    
    def _format_output(self, coordinates: Dict[str, Any]) -> Tuple[str, int, str, str]:
        """
        Format the output in a standardized way.
        
        Args:
            coordinates: Coordinate information
            
        Returns:
            Tuple of (chromosome, position, reference, alternative)
        """
        return (
            coordinates['chrom'],
            coordinates['pos'],
            coordinates['ref'],
            coordinates['alt']
        )
    
    @property
    @abstractmethod
    def supported_prefix(self) -> str:
        """Return the HGVS prefix supported by this parser (e.g., 'g.', 'c.')."""
        pass