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
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match questions
    # Format: (ID) finnish_answer English_text True/False
    pattern = r'\((\d+)\)\s+(oikein|väärin)\s+(.+?)\s+(True|False)'

    matches = re.findall(pattern, content)

    for match in matches:
        question_id, finnish_answer, text, correct_answer = match

        questions.append({
            'id': question_id,
            'module': 'K',
            'type': 'true_false',
            'text': text.strip(),
            'correct_answer': correct_answer == 'True',
            'finnish_answer': finnish_answer
        })

    return questions


def parse_t1_module(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse T1 module questions (Finnish multiple choice format).

    Format example:
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

    for line in lines:
        line = line.strip()

        # Skip empty lines and page markers
        if not line or line.startswith('---') or line.startswith('Sivu'):
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
                'correct_answers': []
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
