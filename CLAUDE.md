# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ham Radio Exam Helper is a web-based study application for Finnish Amateur Radio License exams. It uses a two-phase architecture:

1. **Python parsing phase**: Converts PDF-extracted text files into structured JSON
2. **Static web app phase**: Pure HTML/CSS/JavaScript application that loads JSON data

The project has **no build system** or dependencies beyond Python 3 for parsing. The web app is entirely static and framework-free.

## Data Architecture

### Question Data Flow

```
PDFs → txt files → Python parser → JSON files → JavaScript app
```

- `K-module_in_English.txt`: 245 True/False questions (English)
- `T1_kaikki_kysymykset_v3.txt`: 485 Multiple Choice questions (Finnish)
- `all_questions.json`: Combined database loaded by the web app

### JSON Structure

The `all_questions.json` file has this structure:

```json
{
  "k_module": [
    {
      "id": "20001",
      "module": "K",
      "type": "true_false",
      "text": "Question text...",
      "correct_answer": true,
      "finnish_answer": "oikein"
    }
  ],
  "t1_module": [
    {
      "id": "01001",
      "module": "T1",
      "type": "multiple_choice",
      "text": "Question text...",
      "options": [
        {"letter": "A", "text": "Option text...", "is_correct": true},
        ...
      ],
      "correct_answers": ["A", "B"]
    }
  ]
}
```

**Important**: T1 questions can have multiple correct answers (hence `correct_answers` is an array).

## Common Commands

### Regenerate Question Database

After modifying txt files or parser logic:

```bash
python3 parse_questions.py
```

This regenerates `k_questions.json`, `t1_questions.json`, and `all_questions.json`.

### Run the Application

```bash
python3 -m http.server 8000
# Then open http://localhost:8000
```

The app requires a web server (not just `file://`) because it fetches JSON via `fetch()`.

### Convert New PDFs to Text

If new PDF files are added:

```bash
python3 convert_pdfs.py
```

This uses `pdfplumber` to extract text with page markers.

## Code Architecture

### JavaScript State Management

The app uses a single global `state` object (app.js lines 1-12):

```javascript
const state = {
    selectedModule: null,      // 'K' or 'T1'
    selectedMode: null,        // 'practice', 'exam', or 'study'
    questions: [],             // All questions for selected module
    currentQuestions: [],      // Questions for current session
    currentIndex: 0,
    answers: [],               // User's answers (parallel array to currentQuestions)
    settings: {...}
}
```

**Key pattern**: `questions` holds all module questions, `currentQuestions` holds the subset for the current session (e.g., 60 random questions in exam mode).

### Screen Management

The app has 4 screens (divs with class `screen`):
- `mainMenu`: Module/mode selection
- `questionScreen`: Active quiz/practice
- `resultsScreen`: Score display
- `studyScreen`: Browse mode with answers visible

Only one screen is visible at a time via `display: none/block`.

### Question Display Logic

The `displayQuestion()` function (app.js) handles both question types:

1. Checks `question.type` ('true_false' or 'multiple_choice')
2. Shows/hides appropriate option containers
3. For T1 questions, dynamically generates option buttons from `question.options`
4. Restores previous answers if navigating back

### Answer Validation

- **Practice mode**: Immediate feedback via `showFeedback()` which highlights correct/incorrect options
- **Exam mode**: Only highlights user selection, no feedback until end
- Answers stored in `state.answers` array indexed by question position

## Parser Implementation Details

### K-Module Parser (parse_questions.py)

Uses regex pattern:
```python
r'\((\d+)\)\s+(oikein|väärin)\s+(.+?)\s+(True|False)'
```

Extracts: `(ID) finnish_answer english_text True/False`

### T1-Module Parser

Questions start with `% `, options with ID+Letter+`+`/`-`:
```
01001 % Question text
01001A + correct option
01001B - incorrect option
```

**Critical**: Parser tracks current question ID to group options correctly. Each option line must start with matching question ID.

## Testing Considerations

When modifying the parser:

1. Verify question counts: K should have 245, T1 should have 485
2. Check that T1 questions with multiple correct answers have all stored in `correct_answers` array
3. Test edge cases like questions with 2-6 options (T1 can vary)

When modifying the web app:

1. Test both modules (K true/false UI differs from T1 multiple choice)
2. Test all three modes (practice/exam/study)
3. Verify shuffle options work correctly (questions and T1 option order)
4. Check navigation between questions doesn't lose answers

## File Modification Guidelines

### Modifying Question Sources

- Do not edit JSON files directly - they're generated
- Edit `K-module_in_English.txt` or `T1_kaikki_kysymykset_v3.txt`
- Re-run `parse_questions.py` after changes

### Adding New Features to Web App

The app is intentionally framework-free. When adding features:

- Update the `state` object if new session data is needed
- Use vanilla DOM manipulation (no jQuery/React)
- All styling is in `style.css` - avoid inline styles
- Functions are globally scoped - use descriptive names to avoid collisions

## Exam Rules (from README)

**K-Module exam format**:
- 60 questions randomly selected from 1512 total in official question bank (we have 245 parsed)
- Pass: minimum 45 correct (75%)
- Fail: >4 errors in Emergency Communications and Safety

The app simulates this with 60 random questions from available set, 45/60 pass threshold.
