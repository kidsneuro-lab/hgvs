"""
HGVS parsers using Factory pattern.

This module provides parsers for different HGVS types:
- Genomic (g.)
- Coding DNA (c.)
- Non-coding DNA (n.)
- RNA (r.)
- Protein (p.)
"""
from __future__ import annotations

# Import will be added as we create the modules
try:
    from .factory import HGVSParserFactory
    from .base import BaseHGVSParser
    from .genomic import GenomicParser
    from .coding import CodingParser
    from .noncoding import NonCodingParser
    from .rna import RNAParser
    from .protein import ProteinParser
    
    __all__ = [
        'HGVSParserFactory',
        'BaseHGVSParser',
        'GenomicParser',
        'CodingParser',
        'NonCodingParser',
        'RNAParser',
        'ProteinParser',
    ]
except ImportError:
    # During development, some modules might not exist yet
    __all__ = []