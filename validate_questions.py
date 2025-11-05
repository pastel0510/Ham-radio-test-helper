#!/usr/bin/env python3
"""
Validation script to check for formatting issues and incomplete questions
in the Ham Radio exam question files.
"""

import re
import json

def validate_k_module(filename):
    """Validate K-module questions."""
    print(f"\n=== Validating {filename} ===")
    issues = []
    questions_found = 0

    # Pattern: (ID) finnish_answer english_text True/False
    pattern = r'\((\d+)\)\s+(oikein|väärin)\s+(.+?)\s+(True|False)'

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all question lines (skip page markers)
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines and page markers
        if not line or line.startswith('---') or line.startswith('FINNISH'):
            continue

        # Check if line looks like a question (starts with parenthesis)
        if line.startswith('('):
            match = re.match(pattern, line)
            if match:
                questions_found += 1
                question_id, finnish, text, answer = match.groups()

                # Validate completeness
                if len(text.strip()) < 10:
                    issues.append(f"Line {line_num}: Question {question_id} has very short text: '{text[:50]}'")

                # Check for incomplete sentences
                if not text.strip().endswith(('.', '?', ')', '%', 'Hz', 'kHz', 'MHz', 'GHz', 'W', 'V', 'A', 'Ω', 'm', 's')):
                    issues.append(f"Line {line_num}: Question {question_id} might be incomplete: '{text[:80]}...'")
            else:
                # Line starts with ( but doesn't match pattern
                issues.append(f"Line {line_num}: Malformed question line: '{line[:100]}'")

    print(f"✓ Found {questions_found} questions")

    if issues:
        print(f"\n⚠ Found {len(issues)} potential issues:")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issues")
    else:
        print("✓ No formatting issues found")

    return questions_found, issues

def validate_t1_module(filename):
    """Validate T1-module questions."""
    print(f"\n=== Validating {filename} ===")
    issues = []
    questions = {}
    current_question_id = None

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines, page markers, and section headers
        if not line or line.startswith('---') or line.startswith('Sivu'):
            continue

        # Section header (e.g., "01000 * Section name")
        if ' * ' in line:
            continue

        # Question line (e.g., "01001 % Question text")
        if ' % ' in line:
            match = re.match(r'^(\d{5})\s+%\s+(.+)$', line)
            if match:
                question_id, text = match.groups()
                current_question_id = question_id

                if question_id not in questions:
                    questions[question_id] = {
                        'line': line_num,
                        'text': text,
                        'options': []
                    }
                else:
                    issues.append(f"Line {line_num}: Duplicate question ID {question_id}")

                # Check for very short questions
                if len(text.strip()) < 5:
                    issues.append(f"Line {line_num}: Question {question_id} has very short text: '{text}'")
            else:
                issues.append(f"Line {line_num}: Malformed question line: '{line[:100]}'")

        # Option line (e.g., "01001A + correct option")
        elif re.match(r'^\d{5}[A-Z]', line):
            match = re.match(r'^(\d{5})([A-Z])\s+([+-])\s+(.+)$', line)
            if match:
                question_id, letter, correct_marker, text = match.groups()

                if question_id == current_question_id:
                    if question_id in questions:
                        questions[question_id]['options'].append({
                            'letter': letter,
                            'correct': correct_marker == '+',
                            'text': text,
                            'line': line_num
                        })

                        # Check for very short option text
                        if len(text.strip()) < 2:
                            issues.append(f"Line {line_num}: Option {question_id}{letter} has very short text: '{text}'")
                else:
                    issues.append(f"Line {line_num}: Option {question_id}{letter} doesn't match current question {current_question_id}")
            else:
                issues.append(f"Line {line_num}: Malformed option line: '{line[:100]}'")

    print(f"✓ Found {len(questions)} questions")

    # Check each question for completeness
    incomplete_questions = []
    for qid, qdata in questions.items():
        if len(qdata['options']) < 2:
            incomplete_questions.append(f"Question {qid} (line {qdata['line']}) has only {len(qdata['options'])} option(s)")

        # Check if at least one option is marked correct
        correct_count = sum(1 for opt in qdata['options'] if opt['correct'])
        if correct_count == 0:
            incomplete_questions.append(f"Question {qid} (line {qdata['line']}) has no correct answers")

    if incomplete_questions:
        issues.extend(incomplete_questions)

    if issues:
        print(f"\n⚠ Found {len(issues)} potential issues:")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issues")
    else:
        print("✓ No formatting issues found")

    return len(questions), issues

def validate_json_output():
    """Check the generated JSON file."""
    print("\n=== Validating all_questions.json ===")

    try:
        with open('all_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        k_count = len(data.get('k_module', []))
        t1_count = len(data.get('t1_module', []))

        print(f"✓ JSON is valid")
        print(f"✓ K-module: {k_count} questions")
        print(f"✓ T1-module: {t1_count} questions")

        # Check expected counts
        issues = []
        if k_count != 245:
            issues.append(f"Expected 245 K-module questions, found {k_count}")
        if t1_count != 485:
            issues.append(f"Expected 485 T1-module questions, found {t1_count}")

        return True, issues
    except FileNotFoundError:
        print("⚠ all_questions.json not found - run parse_questions.py first")
        return False, []
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return False, [str(e)]

def main():
    print("=" * 60)
    print("Ham Radio Question Database Validator")
    print("=" * 60)

    # Validate source files
    k_count, k_issues = validate_k_module('K-module_in_English.txt')
    t1_count, t1_issues = validate_t1_module('T1_kaikki_kysymykset_v3.txt')

    # Validate JSON output
    json_valid, json_issues = validate_json_output()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"K-module:  {k_count} questions, {len(k_issues)} issues")
    print(f"T1-module: {t1_count} questions, {len(t1_issues)} issues")
    if json_valid:
        print(f"JSON file: Valid, {len(json_issues)} issues")
    else:
        print("JSON file: Not checked")

    total_issues = len(k_issues) + len(t1_issues) + len(json_issues)
    if total_issues == 0:
        print("\n✓ All validations passed!")
    else:
        print(f"\n⚠ Total: {total_issues} issues found")

    return total_issues

if __name__ == '__main__':
    exit(main())
