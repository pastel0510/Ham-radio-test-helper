#!/usr/bin/env python3
"""
Fix formatting issues in T1 question file.
Replaces em-dashes with regular hyphens.
"""

import re
import shutil
from datetime import datetime

def fix_t1_formatting(filename):
    """Fix em-dashes in T1 file."""

    # Create backup
    backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy(filename, backup_name)
    print(f"Created backup: {backup_name}")

    # Read file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count em-dashes before
    em_dash_count_before = content.count('–')
    print(f"Found {em_dash_count_before} em-dashes (–) to fix")

    # Replace em-dashes with regular hyphens
    # Em-dash: – (U+2013)
    # Regular hyphen: - (U+002D)
    fixed_content = content.replace('–', '-')

    # Count after
    em_dash_count_after = fixed_content.count('–')
    regular_hyphen_count = fixed_content.count(' - ') + fixed_content.count(' + ')

    # Write fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed {em_dash_count_before - em_dash_count_after} em-dashes")
    print(f"File now has approximately {regular_hyphen_count // 2} option lines with +/- markers")
    print(f"✓ {filename} has been fixed")

    return em_dash_count_before - em_dash_count_after

def main():
    print("=" * 60)
    print("Ham Radio Question File Formatter")
    print("=" * 60)

    fixes_made = fix_t1_formatting('T1_kaikki_kysymykset_v3.txt')

    if fixes_made > 0:
        print("\n✓ Formatting fixes completed!")
        print("\nNext steps:")
        print("1. Run: python3 parse_questions.py")
        print("2. Run: python3 validate_questions.py")
    else:
        print("\n✓ No fixes needed - file is already properly formatted")

    return 0

if __name__ == '__main__':
    exit(main())
