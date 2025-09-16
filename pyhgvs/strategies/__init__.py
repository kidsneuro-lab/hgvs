"""
Normalization strategies using Strategy pattern.

This module provides different normalization strategies for HGVS variants:
- Standard VCF normalization
- HGVS-specific normalization
- Custom normalization approaches
"""
from __future__ import annotations

try:
    from .base import BaseNormalizationStrategy
    from .vcf_normalization import VCFNormalizationStrategy
    from .hgvs_normalization import HGVSNormalizationStrategy
    
    __all__ = [
        'BaseNormalizationStrategy',
        'VCFNormalizationStrategy', 
        'HGVSNormalizationStrategy',
    ]
except ImportError:
    __all__ = []