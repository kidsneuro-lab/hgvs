"""
Base HGVS builder using Builder pattern.

This module defines the interface for building HGVS names step by step.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..models.hgvs_name import HGVSName


class BaseHGVSBuilder(ABC):
    """
    Base class for HGVS builders implementing Builder pattern.
    
    Provides a step-by-step approach to constructing complex HGVS names
    with validation at each step.
    """
    
    def __init__(self) -> None:
        """Initialize the builder."""
        self.reset()
    
    def reset(self) -> 'BaseHGVSBuilder':
        """
        Reset the builder to start fresh.
        
        Returns:
            Self for method chaining
        """
        self._hgvs = HGVSName()
        return self
    
    @abstractmethod
    def set_transcript(self, transcript: str) -> 'BaseHGVSBuilder':
        """
        Set the transcript identifier.
        
        Args:
            transcript: Transcript identifier (e.g., 'NM_123456.1')
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def set_gene(self, gene: str) -> 'BaseHGVSBuilder':
        """
        Set the gene name.
        
        Args:
            gene: Gene name
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def set_kind(self, kind: str) -> 'BaseHGVSBuilder':
        """
        Set the HGVS kind (c., g., n., r., p.).
        
        Args:
            kind: HGVS kind
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def set_coordinates(self, start: int, end: Optional[int] = None) -> 'BaseHGVSBuilder':
        """
        Set the coordinates.
        
        Args:
            start: Start coordinate
            end: End coordinate (optional for single position)
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def set_mutation(self, mutation_type: str, ref: str, alt: str) -> 'BaseHGVSBuilder':
        """
        Set the mutation information.
        
        Args:
            mutation_type: Type of mutation (>, ins, del, dup, delins, =)
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Self for method chaining
        """
        pass
    
    def build(self) -> HGVSName:
        """
        Build the final HGVS name.
        
        Returns:
            Complete HGVSName object
            
        Raises:
            ValueError: If required components are missing
        """
        self._validate_build()
        result = self._hgvs
        self.reset()  # Reset for next use
        return result
    
    @abstractmethod
    def _validate_build(self) -> None:
        """
        Validate that all required components are set.
        
        Raises:
            ValueError: If validation fails
        """
        pass