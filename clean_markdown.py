#!/usr/bin/env python3
"""
Markdown File Unicode Normalizer

This script processes Markdown (.md) files to:
1. Preserve all line breaks and formatting structure
2. Normalize Unicode characters using NFKD (Normalization Form Canonical Decomposition)
3. Convert all Unicode characters to ASCII equivalents

Usage:
    python clean_markdown.py input.md output.md
    python clean_markdown.py input.md  # processes in-place
"""

import unicodedata
import argparse
import sys
from pathlib import Path


def normalize_unicode(text):
    """Normalize Unicode characters to ASCII equivalents by removing accents and replacing typographic characters."""
    # First apply NFKD normalization (decomposes accented characters)
    normalized = unicodedata.normalize('NFKD', text)
    
    # Remove combining characters (accent marks) to get pure ASCII base characters
    # Filter out characters in categories 'Mn' (Mark, nonspacing) and 'Mc' (Mark, spacing combining)
    ascii_text = ''.join(char for char in normalized 
                        if unicodedata.category(char) not in ('Mn', 'Mc'))
    
    # Define replacements for common typographic characters
    replacements = {
        # Quotation marks
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201a': "'",  # Single low-9 quotation mark
        '\u201e': '"',  # Double low-9 quotation mark
        '\u2039': "'",  # Single left-pointing angle quotation mark
        '\u203a': "'",  # Single right-pointing angle quotation mark
        '\u00ab': '"',  # Left-pointing double angle quotation mark
        '\u00bb': '"',  # Right-pointing double angle quotation mark
        '\u300e': '"',  # Left white corner bracket
        '\u300f': '"',  # Right white corner bracket
        '\u300c': '"',  # Left corner bracket
        '\u300d': '"',  # Right corner bracket
        
        # Apostrophes
        '\u2019': "'",  # Right single quotation mark (apostrophe)
        '`': "'",       # Grave accent (used as apostrophe)
        '\u00b4': "'",  # Acute accent (used as apostrophe)
        '\u02bc': "'",  # Modifier letter apostrophe
        '\u02bb': "'",  # Modifier letter turned comma
        
        # Dashes
        '\u2014': '-',  # Em dash
        '\u2013': '-',  # En dash
        '\u2212': '-',  # Minus sign
        '\u2012': '-',  # Figure dash
        '\u2e3a': '-',  # Two-em dash
        '\u2e3b': '-',  # Three-em dash
        '\ufe58': '-',  # Small em dash
        '\ufe63': '-',  # Small hyphen-minus
        
        # Other common typographic characters
        '\u2026': '...',  # Horizontal ellipsis
        '\u2030': '%o',   # Per mille sign
        '\u2031': '%oo',  # Per ten thousand sign
        '\u2032': "'",    # Prime (often used as apostrophe)
        '\u2033': '"',    # Double prime (often used as quote)
        '\u2034': "'''",  # Triple prime
        '\u2057': "''''", # Quadruple prime
    }
    
    # Apply character replacements to the ASCII text
    for original, replacement in replacements.items():
        ascii_text = ascii_text.replace(original, replacement)
    
    # Additional mappings for characters that might not be handled by NFKD
    additional_mappings = {
        # Currency symbols
        '€': 'EUR',
        '£': 'GBP', 
        '¥': 'JPY',
        '¢': 'c',
        '₹': 'Rs',
        '₽': 'Rub',
        
        # Mathematical symbols
        '×': 'x',
        '÷': '/',
        '±': '+/-',
        '°': 'deg',
        '²': '2',
        '³': '3',
        '¼': '1/4',
        '½': '1/2',  
        '¾': '3/4',
        '⅐': '1/7',
        '⅑': '1/9', 
        '⅒': '1/10',
        '⅓': '1/3',
        '⅔': '2/3',
        '⅕': '1/5',
        '⅖': '2/5',
        '⅗': '3/5',
        '⅘': '4/5',
        '⅙': '1/6',
        '⅚': '5/6',
        '⅛': '1/8',
        '⅜': '3/8',
        '⅝': '5/8',
        '⅞': '7/8',
        
        # Other common symbols
        '©': '(c)',
        '®': '(r)',
        '™': 'TM',
        '§': 'section',
        '¶': 'P',
        '†': '+',
        '‡': '++',
        
        # Letters that might not decompose properly
        'ß': 'ss',
        'æ': 'ae',
        'œ': 'oe',
        'Æ': 'AE',
        'Œ': 'OE',
        'ð': 'd',
        'þ': 'th',
        'Ð': 'D',
        'Þ': 'Th',
        'ø': 'o',
        'Ø': 'O',
        'ł': 'l',
        'Ł': 'L',
        
        # Common Greek letters
        'α': 'alpha',
        'β': 'beta', 
        'γ': 'gamma',
        'δ': 'delta',
        'ε': 'epsilon',
        'ζ': 'zeta',
        'η': 'eta',
        'θ': 'theta',
        'ι': 'iota',
        'κ': 'kappa',
        'λ': 'lambda',
        'μ': 'mu',
        'ν': 'nu',
        'ξ': 'xi',
        'ο': 'omicron',
        'π': 'pi',
        'ρ': 'rho',
        'σ': 'sigma',
        'τ': 'tau',
        'υ': 'upsilon',
        'φ': 'phi',
        'χ': 'chi',
        'ψ': 'psi',
        'ω': 'omega',
        'Α': 'Alpha',
        'Β': 'Beta',
        'Γ': 'Gamma',
        'Δ': 'Delta',
        'Ε': 'Epsilon',
        'Ζ': 'Zeta',
        'Η': 'Eta',
        'Θ': 'Theta',
        'Ι': 'Iota',
        'Κ': 'Kappa',
        'Λ': 'Lambda',
        'Μ': 'Mu',
        'Ν': 'Nu',
        'Ξ': 'Xi',
        'Ο': 'Omicron',
        'Π': 'Pi',
        'Ρ': 'Rho',
        'Σ': 'Sigma',
        'Τ': 'Tau',
        'Υ': 'Upsilon',
        'Φ': 'Phi',
        'Χ': 'Chi',
        'Ψ': 'Psi',
        'Ω': 'Omega',
        
        # Arrows and other symbols
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '↔': '<->',
        '⇒': '=>',
        '⇐': '<=',
        '⇔': '<=>',
        '∞': 'infinity',
        '≈': '~=',
        '≠': '!=',
        '≤': '<=',
        '≥': '>=',
    }
    
    # Apply additional mappings
    for original, replacement in additional_mappings.items():
        ascii_text = ascii_text.replace(original, replacement)
    
    # Final safety check: replace any remaining non-ASCII characters with '?'
    # This ensures we truly get ASCII-only output
    final_ascii = ''.join(char if ord(char) < 128 else '?' for char in ascii_text)
    
    return final_ascii


def clean_markdown_file(input_path, output_path=None):
    """
    Clean Markdown file by normalizing Unicode to ASCII while preserving structure.
    
    Args:
        input_path (str): Path to input Markdown file
        output_path (str, optional): Path to output file. If None, processes in-place.
    
    Returns:
        tuple: (lines_processed, characters_replaced)
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Use temporary file for in-place processing
    if output_path is None:
        output_path = input_path.with_suffix(input_path.suffix + '.tmp')
        process_in_place = True
    else:
        output_path = Path(output_path)
        process_in_place = False
    
    lines_processed = 0
    characters_replaced = 0
    
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                lines_processed += 1
                
                # Normalize Unicode characters in the line
                original_line = line
                normalized_line = normalize_unicode(line)
                
                # Count characters that were changed
                if original_line != normalized_line:
                    characters_replaced += sum(1 for a, b in zip(original_line, normalized_line) if a != b)
                    # Account for length differences (some chars become multiple chars)
                    characters_replaced += abs(len(original_line) - len(normalized_line))
                
                # Write the line (including newlines and empty lines)
                outfile.write(normalized_line)
        
        # Replace original file if processing in-place
        if process_in_place:
            output_path.replace(input_path)
            
    except Exception as e:
        # Clean up temporary file if something goes wrong
        if process_in_place and output_path.exists():
            output_path.unlink()
        raise e
    
    return lines_processed, characters_replaced


def main():
    parser = argparse.ArgumentParser(
        description="Clean Markdown files by normalizing Unicode characters to ASCII equivalents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md cleaned_document.md    # Save to new file
  %(prog)s document.md                        # Process in-place
  %(prog)s --verbose document.md output.md    # Show detailed progress
        """
    )
    
    parser.add_argument('input_file', help='Input Markdown file path')
    parser.add_argument('output_file', nargs='?', help='Output Markdown file path (optional, defaults to in-place)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    # Validate input file extension
    input_path = Path(args.input_file)
    if input_path.suffix.lower() not in ['.md', '.markdown']:
        print(f"Warning: Input file doesn't have .md or .markdown extension: {input_path}", file=sys.stderr)
    
    try:
        if args.dry_run:
            print(f"DRY RUN: Would process {args.input_file}")
            if args.output_file:
                print(f"DRY RUN: Would save results to {args.output_file}")
            else:
                print("DRY RUN: Would process in-place")
            return
        
        if args.verbose:
            action = "in-place" if not args.output_file else f"to {args.output_file}"
            print(f"Processing Markdown file {args.input_file} {action}...")
        
        lines_processed, characters_replaced = clean_markdown_file(
            args.input_file, 
            args.output_file
        )
        
        if args.verbose or not args.output_file:
            print(f"Processed {lines_processed} lines")
            print(f"Normalized {characters_replaced} Unicode characters to ASCII")
        
        print("✅ Markdown file cleaned successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
