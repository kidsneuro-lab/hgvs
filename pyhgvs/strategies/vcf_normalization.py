"""
VCF normalization strategy.

Implements VCF-style normalization according to VCF specification.
"""
from __future__ import annotations

from typing import Any, Tuple

from .base import BaseNormalizationStrategy
from ..models.variants import normalize_variant


class VCFNormalizationStrategy(BaseNormalizationStrategy):
    """
    VCF normalization strategy.
    
    Implements standard VCF normalization:
    - Left-align indels
    - Minimal representation
    - Standard padding
    """
    
    def __init__(self, genome: Any, flank_length: int = 30) -> None:
        """
        Initialize VCF normalization strategy.
        
        Args:
            genome: Genome sequence data
            flank_length: Length of flanking sequence for normalization
        """
        super().__init__(genome)
        self.flank_length = flank_length
    
    def normalize(
        self,
        chrom: str,
        pos: int,
        ref: str,
        alt: str,
        **kwargs
    ) -> Tuple[str, int, str, str]:
        """
        Normalize variant using VCF standard.
        
        Args:
            chrom: Chromosome name
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            **kwargs: Additional options (indels_start_with_same_base, etc.)
            
        Returns:
            Tuple of normalized variant components
        """
        self.validate_input(chrom, pos, ref, alt)
        
        # Use existing normalize_variant function
        flank_length = kwargs.get('flank_length', self.flank_length)
        indels_start_with_same_base = kwargs.get('indels_start_with_same_base', True)
        
        normalized = normalize_variant(
            chrom=chrom,
            offset=pos,
            ref=ref,
            alts=[alt],
            genome=self.genome,
            flank_length=flank_length,
            indels_start_with_same_base=indels_start_with_same_base
        )
        
        return normalized.variant[0], normalized.variant[1], normalized.variant[2], normalized.variant[3][0]
    
    def get_strategy_name(self) -> str:
        """Return the strategy name."""
        return "VCF Normalization"