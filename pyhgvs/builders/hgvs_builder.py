"""
HGVS name builder implementation.

Provides a concrete implementation of the Builder pattern for HGVS names.
"""
from __future__ import annotations

from typing import Optional

from .base import BaseHGVSBuilder


class HGVSNameBuilder(BaseHGVSBuilder):
    """
    Concrete implementation of HGVS name builder.
    
    Allows step-by-step construction of HGVS names with validation.
    """
    
    def set_transcript(self, transcript: str) -> 'HGVSNameBuilder':
        """
        Set the transcript identifier.
        
        Args:
            transcript: Transcript identifier (e.g., 'NM_123456.1')
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If transcript format is invalid
        """
        if not transcript or not isinstance(transcript, str):
            raise ValueError("Transcript must be a non-empty string")
        
        self._hgvs.transcript = transcript
        return self
    
    def set_gene(self, gene: str) -> 'HGVSNameBuilder':
        """
        Set the gene name.
        
        Args:
            gene: Gene name
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If gene format is invalid
        """
        if not gene or not isinstance(gene, str):
            raise ValueError("Gene must be a non-empty string")
        
        self._hgvs.gene = gene
        return self
    
    def set_kind(self, kind: str) -> 'HGVSNameBuilder':
        """
        Set the HGVS kind.
        
        Args:
            kind: HGVS kind (c, g, n, r, p)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If kind is not supported
        """
        valid_kinds = {'c', 'g', 'n', 'r', 'p'}
        if kind not in valid_kinds:
            raise ValueError(f"Kind must be one of {valid_kinds}, got '{kind}'")
        
        self._hgvs.kind = kind
        return self
    
    def set_coordinates(self, start: int, end: Optional[int] = None) -> 'HGVSNameBuilder':
        """
        Set the coordinates.
        
        Args:
            start: Start coordinate
            end: End coordinate (optional)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If coordinates are invalid
        """
        if not isinstance(start, int) or start < 1:
            raise ValueError("Start coordinate must be a positive integer")
        
        if end is not None:
            if not isinstance(end, int) or end < start:
                raise ValueError("End coordinate must be an integer >= start coordinate")
        
        self._hgvs.start = start
        self._hgvs.end = end if end is not None else start
        
        return self
    
    def set_cdna_coordinates(self, start_coord: int, end_coord: Optional[int] = None,
                            start_offset: Optional[int] = None, end_offset: Optional[int] = None) -> 'HGVSNameBuilder':
        """
        Set cDNA coordinates with optional offsets.
        
        Args:
            start_coord: Start coordinate
            end_coord: End coordinate (optional)
            start_offset: Start offset from coordinate
            end_offset: End offset from coordinate
            
        Returns:
            Self for method chaining
        """
        from ..models.cdna import CDNACoord
        
        self._hgvs.cdna_start = CDNACoord(start_coord, start_offset)
        if end_coord is not None:
            self._hgvs.cdna_end = CDNACoord(end_coord, end_offset)
        else:
            self._hgvs.cdna_end = self._hgvs.cdna_start
        
        return self
    
    def set_mutation(self, mutation_type: str, ref: str, alt: str) -> 'HGVSNameBuilder':
        """
        Set the mutation information.
        
        Args:
            mutation_type: Type of mutation
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If mutation parameters are invalid
        """
        valid_types = {'>', 'ins', 'del', 'dup', 'delins', '='}
        if mutation_type not in valid_types:
            raise ValueError(f"Mutation type must be one of {valid_types}, got '{mutation_type}'")
        
        if not isinstance(ref, str):
            raise ValueError("Reference allele must be a string")
        
        if not isinstance(alt, str):
            raise ValueError("Alternative allele must be a string")
        
        self._hgvs.mutation_type = mutation_type
        self._hgvs.ref_allele = ref
        self._hgvs.alt_allele = alt
        
        return self
    
    def _validate_build(self) -> None:
        """
        Validate that all required components are set.
        
        Raises:
            ValueError: If validation fails
        """
        if not self._hgvs.kind:
            raise ValueError("HGVS kind must be set")
        
        if not self._hgvs.mutation_type:
            raise ValueError("Mutation type must be set")
        
        # Check coordinates based on kind
        if self._hgvs.kind in ('c', 'n', 'r'):
            if not self._hgvs.cdna_start:
                raise ValueError("cDNA coordinates must be set for kind '{}'".format(self._hgvs.kind))
        else:
            if not self._hgvs.start:
                raise ValueError("Genomic coordinates must be set for kind '{}'".format(self._hgvs.kind))
    
    @classmethod
    def create_simple_substitution(cls, chrom: str, pos: int, ref: str, alt: str) -> 'HGVSNameBuilder':
        """
        Create a builder for a simple substitution.
        
        Args:
            chrom: Chromosome
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Configured builder
        """
        return (cls()
                .set_kind('g')
                .set_coordinates(pos)
                .set_mutation('>', ref, alt))
    
    @classmethod
    def create_coding_variant(cls, transcript: str, pos: int, ref: str, alt: str) -> 'HGVSNameBuilder':
        """
        Create a builder for a coding variant.
        
        Args:
            transcript: Transcript identifier
            pos: cDNA position
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Configured builder
        """
        return (cls()
                .set_transcript(transcript)
                .set_kind('c')
                .set_cdna_coordinates(pos)
                .set_mutation('>', ref, alt))