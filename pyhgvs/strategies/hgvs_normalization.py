"""
HGVS normalization strategy.

Implements HGVS-specific normalization according to HGVS recommendations.
"""
from __future__ import annotations

from typing import Any, Optional, Tuple

from .base import BaseNormalizationStrategy
from .. import hgvs_normalize_variant


class HGVSNormalizationStrategy(BaseNormalizationStrategy):
    """
    HGVS normalization strategy.
    
    Implements HGVS-specific normalization:
    - 3' justification for indels
    - Duplication representation when appropriate
    - HGVS coordinate system
    """
    
    def __init__(self, genome: Any, transcript: Optional[Any] = None) -> None:
        """
        Initialize HGVS normalization strategy.
        
        Args:
            genome: Genome sequence data
            transcript: Optional transcript for strand-specific normalization
        """
        super().__init__(genome)
        self.transcript = transcript
    
    def normalize(
        self,
        chrom: str,
        pos: int,
        ref: str,
        alt: str,
        **kwargs
    ) -> Tuple[str, int, str, str]:
        """
        Normalize variant using HGVS standard.
        
        Args:
            chrom: Chromosome name
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            **kwargs: Additional options
            
        Returns:
            Tuple of normalized variant components
        """
        self.validate_input(chrom, pos, ref, alt)
        
        # Use existing HGVS normalization function
        transcript = kwargs.get('transcript', self.transcript)
        
        norm_chrom, norm_pos, norm_ref, norm_alt, mutation_type = hgvs_normalize_variant(
            chrom=chrom,
            offset=pos,
            ref=ref,
            alt=alt,
            genome=self.genome,
            transcript=transcript
        )
        
        return norm_chrom, norm_pos, norm_ref, norm_alt
    
    def get_strategy_name(self) -> str:
        """Return the strategy name."""
        return "HGVS Normalization"