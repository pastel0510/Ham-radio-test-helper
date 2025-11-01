#!/usr/bin/env python3
"""
Script to convert PDF files to text format with proper formatting.
"""

import sys
from pathlib import Path
import pdfplumber


def convert_pdf_to_text(pdf_path: str, output_path: str = None) -> None:
    """
    Convert a PDF file to text format.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional output path. If not provided, uses the same name with .txt extension
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    if output_path is None:
        output_path = pdf_file.with_suffix('.txt')
    else:
        output_path = Path(output_path)

    print(f"Converting {pdf_file.name} to {output_path.name}...")

    try:
        # Open the PDF with pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and text.strip():  # Only add non-empty pages
                    text_content.append(f"--- Page {page_num} ---\n")
                    text_content.append(text)
                    text_content.append("\n\n")

            # Write to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(text_content)

            print(f"✓ Successfully converted {pdf_file.name}")
            print(f"  Output: {output_path}")
            print(f"  Pages: {len(pdf.pages)}")

    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        sys.exit(1)


def main():
    """Main function to convert all PDFs in the current directory."""
    current_dir = Path(__file__).parent

    # Find all PDF files
    pdf_files = list(current_dir.glob('*.pdf'))

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return

    print(f"Found {len(pdf_files)} PDF file(s):\n")

    # Convert each PDF
    for pdf_file in pdf_files:
        convert_pdf_to_text(str(pdf_file))
        print()

    print("All conversions completed!")


if __name__ == "__main__":
    main()
