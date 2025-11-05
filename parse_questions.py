#!/usr/bin/env python3
"""
Parser for Ham Radio exam questions.
Converts K-module and T1 module questions to JSON format.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any


def parse_k_module(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse K-module questions (English true/false format).

    Format example:
    (20001) oikein DL is the amateur radio prefix used for Germany. True

    Categories are encoded in the question ID:
    - Category number = (first 2 digits of ID) - 19
    - E.g., ID 20001 → Category 1, ID 40001 → Category 20
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse category headers to build a mapping
    # Format: "1. MAATUNNUKSET 1. COUNTRY PREFIXES"
    # Note: Some headers have variations like "4- Q-LYHENTEET" or "12.CERTIFICATE" (no space)
    category_pattern = r'^(\d+)[\.\-]\s*([A-ZÄÖÅ\s\-]+?)\s+\d+\.?\s*([A-Z\s\-]+(?:\([^)]*\))?)\s*$'
    categories = {}

    for line in content.split('\n'):
        cat_match = re.match(category_pattern, line.strip())
        if cat_match:
            cat_num = int(cat_match.group(1))
            finnish_name = cat_match.group(2).strip()
            english_name = cat_match.group(3).strip()
            categories[cat_num] = {
                'number': cat_num,
                'finnish_name': finnish_name,
                'english_name': english_name
            }

    # Pattern to match questions (single-line format only)
    # Format: (ID) finnish_answer English_text True/False
    # Note: The source file has 1500+ questions, but only 245 are in the
    # properly formatted single-line English translation format. This appears
    # to be intentional - a curated subset for the study app.
    pattern = r'\((\d+)\)\s+(oikein|väärin)\s+(.+?)\s+(True|False)'

    matches = re.findall(pattern, content)

    for match in matches:
        question_id, finnish_answer, text, correct_answer = match

        # Derive category from question ID
        # The mapping is: 20→1, 21→2, ..., 38→19, 40→20, 41→21 (skips 39)
        id_prefix = int(question_id[:2])
        if id_prefix <= 38:
            category_num = id_prefix - 19
        else:  # id_prefix >= 40
            category_num = id_prefix - 20

        category_info = categories.get(category_num, {
            'number': category_num,
            'finnish_name': 'Unknown',
            'english_name': 'Unknown'
        })

        questions.append({
            'id': question_id,
            'module': 'K',
            'type': 'true_false',
            'text': text.strip(),
            'correct_answer': correct_answer == 'True',
            'finnish_answer': finnish_answer,
            'category': category_info['english_name'],
            'category_number': category_num,
            'category_finnish': category_info['finnish_name']
        })

    return questions


def parse_t1_module(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse T1 module questions (Finnish multiple choice format).

    Format example:
    01000 * Category name
    01001 % Question text
    01001A + option A
    01001B + option B
    01001C - option C
    01001D - option D
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_question = None
    current_category = None
    current_category_number = None

    for line in lines:
        line = line.strip()

        # Skip empty lines and page markers
        if not line or line.startswith('---') or line.startswith('Sivu'):
            continue

        # Category line (starts with ID + asterisk)
        # Format: 01000 * Category name
        category_match = re.match(r'^(\d+)\s+\*\s+(.+)$', line)
        if category_match:
            category_id = category_match.group(1)
            category_name = category_match.group(2).strip()
            # Category number is first 2 digits of ID (01000 → 01, 02000 → 02)
            current_category_number = int(category_id[:2])
            current_category = category_name
            continue

        # Question text (starts with question ID and %)
        question_match = re.match(r'^(\d+)\s+%\s+(.+)$', line)
        if question_match:
            if current_question and current_question['options']:
                questions.append(current_question)

            question_id = question_match.group(1)
            question_text = question_match.group(2)

            current_question = {
                'id': question_id,
                'module': 'T1',
                'type': 'multiple_choice',
                'text': question_text,
                'options': [],
                'correct_answers': [],
                'category': current_category if current_category else 'Unknown',
                'category_number': current_category_number if current_category_number else 0
            }
            continue

        # Option line (starts with question ID + letter + +/-)
        if current_question:
            option_match = re.match(r'^(\d+)([A-F])\s+([+\-])\s+(.+)$', line)
            if option_match:
                question_id, letter, is_correct, option_text = option_match.groups()

                # Make sure this option belongs to current question
                if question_id == current_question['id']:
                    current_question['options'].append({
                        'letter': letter,
                        'text': option_text,
                        'is_correct': is_correct == '+'
                    })

                    if is_correct == '+':
                        current_question['correct_answers'].append(letter)

    # Add the last question
    if current_question and current_question['options']:
        questions.append(current_question)

    return questions


def main():
    """Parse both question files and save to JSON."""

    base_dir = Path(__file__).parent

    print("Parsing K-module questions...")
    k_questions = parse_k_module(str(base_dir / 'K-module_in_English.txt'))
    print(f"  Found {len(k_questions)} K-module questions")

    print("\nParsing T1 module questions...")
    t1_questions = parse_t1_module(str(base_dir / 'T1_kaikki_kysymykset_v3.txt'))
    print(f"  Found {len(t1_questions)} T1 module questions")

    # Save to JSON files
    print("\nSaving to JSON files...")

    with open(base_dir / 'k_questions.json', 'w', encoding='utf-8') as f:
        json.dump(k_questions, f, ensure_ascii=False, indent=2)
    print("  Saved k_questions.json")

    with open(base_dir / 't1_questions.json', 'w', encoding='utf-8') as f:
        json.dump(t1_questions, f, ensure_ascii=False, indent=2)
    print("  Saved t1_questions.json")

    # Save combined file
    all_questions = {
        'k_module': k_questions,
        't1_module': t1_questions
    }

    with open(base_dir / 'all_questions.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print("  Saved all_questions.json")

    print("\n✓ Parsing complete!")
    print(f"\nSummary:")
    print(f"  K-module:  {len(k_questions)} questions (True/False)")
    print(f"  T1 module: {len(t1_questions)} questions (Multiple Choice)")
    print(f"  Total:     {len(k_questions) + len(t1_questions)} questions")


if __name__ == "__main__":
    main()
