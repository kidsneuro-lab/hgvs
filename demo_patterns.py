#!/usr/bin/env python3
"""
Demonstration of the new design patterns in pyhgvs.

This script shows how to use the Factory, Strategy, and Builder patterns
that have been added to improve maintainability.
"""
from __future__ import annotations

def demonstrate_factory_pattern():
    """Demonstrate the Factory pattern for HGVS parsers."""
    print("=== Factory Pattern Demo ===")
    
    from pyhgvs.parsers.factory import HGVSParserFactory
    
    # Show supported types
    supported = HGVSParserFactory.get_supported_types()
    print(f"Supported HGVS types: {supported}")
    
    # Auto-detect HGVS type
    test_hgvs = "NC_000001.11:g.123456A>T"
    detected_type = HGVSParserFactory.detect_hgvs_type(test_hgvs)
    print(f"Detected type for '{test_hgvs}': {detected_type}")
    
    # Create parser for genomic HGVS
    # Note: This is a demonstration - normally you'd pass a real genome object
    try:
        parser = HGVSParserFactory.create_parser(detected_type, genome=None)
        print(f"✓ Created parser: {parser.__class__.__name__}")
        print(f"  Supports prefix: {parser.supported_prefix}")
    except Exception as e:
        print(f"Parser creation demo (expected without genome): {e}")
    
    print()

def demonstrate_strategy_pattern():
    """Demonstrate the Strategy pattern for normalization."""
    print("=== Strategy Pattern Demo ===")
    
    from pyhgvs.strategies.base import BaseNormalizationStrategy
    from pyhgvs.strategies.vcf_normalization import VCFNormalizationStrategy
    from pyhgvs.strategies.hgvs_normalization import HGVSNormalizationStrategy
    
    # Show strategy names
    # Note: This is a demonstration - normally you'd pass a real genome object
    try:
        vcf_strategy = VCFNormalizationStrategy(genome=None)
        hgvs_strategy = HGVSNormalizationStrategy(genome=None)
        
        print(f"Available strategies:")
        print(f"  - {vcf_strategy.get_strategy_name()}")
        print(f"  - {hgvs_strategy.get_strategy_name()}")
        
        # Show how you could switch strategies at runtime
        print("✓ Strategies can be switched at runtime for different normalization approaches")
        
    except Exception as e:
        print(f"Strategy demo (expected without genome): {e}")
    
    print()

def demonstrate_builder_pattern():
    """Demonstrate the Builder pattern for HGVS construction."""
    print("=== Builder Pattern Demo ===")
    
    from pyhgvs.builders.hgvs_builder import HGVSNameBuilder
    
    # Build a simple genomic substitution
    try:
        hgvs = (HGVSNameBuilder()
                .set_kind('g')
                .set_coordinates(123456)
                .set_mutation('>', 'A', 'T')
                .build())
        
        print(f"✓ Built genomic substitution:")
        print(f"  Kind: {hgvs.kind}")
        print(f"  Position: {hgvs.start}")
        print(f"  Mutation: {hgvs.ref_allele}>{hgvs.alt_allele}")
        
    except Exception as e:
        print(f"Builder demo error: {e}")
    
    # Build a coding variant
    try:
        hgvs2 = (HGVSNameBuilder()
                 .set_transcript('NM_123456.1')
                 .set_kind('c')
                 .set_cdna_coordinates(100)
                 .set_mutation('>', 'C', 'G')
                 .build())
        
        print(f"✓ Built coding variant:")
        print(f"  Transcript: {hgvs2.transcript}")
        print(f"  Kind: {hgvs2.kind}")
        print(f"  cDNA position: {hgvs2.cdna_start.coord if hgvs2.cdna_start else 'None'}")
        
    except Exception as e:
        print(f"Builder demo error: {e}")
    
    # Show validation in action
    try:
        incomplete_builder = HGVSNameBuilder().set_kind('g')
        incomplete_builder.build()  # This should fail
    except ValueError as e:
        print(f"✓ Builder validation works: {e}")
    
    print()

def demonstrate_backward_compatibility():
    """Show that existing API still works."""
    print("=== Backward Compatibility Demo ===")
    
    import pyhgvs
    from pyhgvs.models.hgvs_name import HGVSName
    
    # Test existing functionality
    hgvs = HGVSName("NC_000001.11:g.123456A>T")
    print(f"✓ Original HGVSName parsing still works:")
    print(f"  Parsed: {hgvs.kind}.{hgvs.start}{hgvs.ref_allele}>{hgvs.alt_allele}")
    
    # Test that all original functions are still available
    functions = ['get_genomic_sequence', 'get_allele', 'get_vcf_allele', 
                'parse_hgvs_name', 'format_hgvs_name', 'variant_to_hgvs_name']
    
    available = [func for func in functions if hasattr(pyhgvs, func)]
    print(f"✓ Original API functions available: {len(available)}/{len(functions)}")
    
    print()

def main():
    """Run all demonstrations."""
    print("HGVS Design Patterns Demonstration")
    print("=" * 40)
    print()
    
    demonstrate_factory_pattern()
    demonstrate_strategy_pattern()
    demonstrate_builder_pattern()
    demonstrate_backward_compatibility()
    
    print("Benefits of the new design:")
    print("- Factory Pattern: Easy to add new HGVS types")
    print("- Strategy Pattern: Flexible normalization approaches") 
    print("- Builder Pattern: Safe construction of complex HGVS names")
    print("- Template Method: Consistent processing workflow")
    print("- All original APIs preserved for backward compatibility")

if __name__ == "__main__":
    main()