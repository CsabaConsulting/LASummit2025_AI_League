#!/usr/bin/env python3
"""
JSONL File Cleaner and Unicode Normalizer

This script processes JSONL (JSON Lines) files to:
1. Remove empty lines and lines containing only whitespace
2. Normalize Unicode characters using NFKD (Normalization Form Canonical Decomposition)

Usage:
    python clean_jsonl.py input.jsonl output.jsonl
    python clean_jsonl.py input.jsonl  # processes in-place
"""

import json
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


def process_json_value(value):
    """Recursively process JSON values to normalize Unicode strings."""
    if isinstance(value, str):
        return normalize_unicode(value)
    elif isinstance(value, dict):
        return {k: process_json_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_json_value(item) for item in value]
    else:
        return value


def clean_jsonl_file(input_path, output_path=None):
    """
    Clean JSONL file by removing empty lines and normalizing Unicode.
    
    Args:
        input_path (str): Path to input JSONL file
        output_path (str, optional): Path to output file. If None, processes in-place.
    
    Returns:
        tuple: (lines_processed, lines_removed, lines_written)
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
    lines_removed = 0
    lines_written = 0
    
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            for line_num, line in enumerate(infile, 1):
                lines_processed += 1
                
                # Skip empty lines or lines with only whitespace
                if not line.strip():
                    lines_removed += 1
                    continue
                
                try:
                    # Parse JSON to validate and process
                    json_obj = json.loads(line.strip())
                    
                    # Normalize Unicode characters in the JSON object
                    normalized_obj = process_json_value(json_obj)
                    
                    # Write normalized JSON back to file
                    json.dump(normalized_obj, outfile, ensure_ascii=False, separators=(',', ':'))
                    outfile.write('\n')
                    lines_written += 1
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON on line {line_num}: {e}", file=sys.stderr)
                    print(f"  Line content: {line.strip()[:100]}...", file=sys.stderr)
                    lines_removed += 1
                    continue
        
        # Replace original file if processing in-place
        if process_in_place:
            output_path.replace(input_path)
            
    except Exception as e:
        # Clean up temporary file if something goes wrong
        if process_in_place and output_path.exists():
            output_path.unlink()
        raise e
    
    return lines_processed, lines_removed, lines_written


def main():
    parser = argparse.ArgumentParser(
        description="Clean JSONL files by removing empty lines and normalizing Unicode characters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.jsonl cleaned_data.jsonl    # Save to new file
  %(prog)s data.jsonl                       # Process in-place
  %(prog)s --verbose data.jsonl output.jsonl  # Show detailed progress
        """
    )
    
    parser.add_argument('input_file', help='Input JSONL file path')
    parser.add_argument('output_file', nargs='?', help='Output JSONL file path (optional, defaults to in-place)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
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
            print(f"Processing {args.input_file} {action}...")
        
        lines_processed, lines_removed, lines_written = clean_jsonl_file(
            args.input_file, 
            args.output_file
        )
        
        if args.verbose or not args.output_file:
            print(f"Processed {lines_processed} lines")
            print(f"Removed {lines_removed} empty/invalid lines")
            print(f"Written {lines_written} clean lines")
            
            if lines_removed > 0:
                print(f"Removed {lines_removed / lines_processed * 100:.1f}% of lines")
        
        print("✅ JSONL file cleaned successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
