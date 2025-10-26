"""
Base normalization strategy using Strategy pattern.

This module defines the interface for different normalization approaches.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class BaseNormalizationStrategy(ABC):
    """
    Base class for normalization strategies implementing Strategy pattern.
    
    Defines the interface for different normalization approaches while
    allowing flexible switching between strategies at runtime.
    """
    
    def __init__(self, genome: Any) -> None:
        """
        Initialize the normalization strategy.
        
        Args:
            genome: Genome sequence data for normalization
        """
        self.genome = genome
    
    @abstractmethod
    def normalize(
        self,
        chrom: str,
        pos: int,
        ref: str,
        alt: str,
        **kwargs
    ) -> Tuple[str, int, str, str]:
        """
        Normalize a variant.
        
        Args:
            chrom: Chromosome name
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            **kwargs: Additional strategy-specific options
            
        Returns:
            Tuple of (normalized_chrom, normalized_pos, normalized_ref, normalized_alt)
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Get the name of this normalization strategy.
        
        Returns:
            Strategy name for identification
        """
        pass
    
    def validate_input(
        self,
        chrom: str,
        pos: int,
        ref: str,
        alt: str
    ) -> None:
        """
        Validate input parameters.
        
        Args:
            chrom: Chromosome name
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            
        Raises:
            ValueError: If input parameters are invalid
        """
        if not chrom:
            raise ValueError("Chromosome name cannot be empty")
        if pos < 1:
            raise ValueError("Position must be positive")
        if not ref:
            raise ValueError("Reference allele cannot be empty")
        if not alt:
            raise ValueError("Alternative allele cannot be empty")