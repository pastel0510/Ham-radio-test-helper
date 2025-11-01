# Ham Radio Exam Helper

A comprehensive web application for preparing for Finnish Amateur Radio License exams (K-module and T1-module).

## Features

### Modules Supported
- **K Module**: 245 True/False questions in English
- **T1 Module**: 485 Multiple Choice questions in Finnish

### Study Modes

1. **Practice Mode**
   - Work through questions with immediate feedback
   - See correct answers after each question
   - Learn as you go

2. **Exam Mode**
   - Simulate real exam conditions
   - 60 randomly selected questions
   - Results shown at the end
   - Pass threshold: 45/60 correct answers

3. **Study Mode**
   - Browse all questions with answers visible
   - Perfect for reviewing material

### Settings
- Shuffle questions (randomize order)
- Shuffle options (randomize answer choices for T1 questions)

## File Structure

```
Ham-radio-test-helper/
├── index.html              # Main HTML file
├── style.css               # Styling
├── app.js                  # Application logic
├── parse_questions.py      # Python script to parse txt files
├── convert_pdfs.py         # PDF to text converter
├── K-module_in_English.txt # K-module questions (English)
├── T1_kaikki_kysymykset_v3.txt # T1 questions (Finnish)
├── k_questions.json        # Parsed K-module questions
├── t1_questions.json       # Parsed T1 questions
└── all_questions.json      # Combined question database
```

## Usage

### Setup

1. Parse the question files (if not already done):
```bash
python3 parse_questions.py
```

This will generate:
- `k_questions.json`
- `t1_questions.json`
- `all_questions.json`

### Running the Application

1. Start a local web server:
```bash
python3 -m http.server 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Select your module (K or T1), choose a mode (Practice/Exam/Study), and start!

## Question Format

### K-Module (True/False)
- 245 questions in English
- Each question is a statement to be marked as True or False
- Covers topics like country prefixes, Q-codes, operating procedures, regulations, etc.

### T1-Module (Multiple Choice)
- 485 questions in Finnish
- Each question may have multiple correct answers
- Covers technical topics: electricity, electronics, radio theory, regulations, etc.

## Exam Information

### K-Module Exam
- 60 questions selected randomly from 1512 question bank
- Pass requirement: minimum 45 correct answers (75%)
- Fail condition: more than 4 errors in Emergency Communications and Safety
- Questions are True/False format

### T1-Module Exam
- 60 questions selected from the question bank
- Pass requirement: minimum 45 correct answers (75%)
- Multiple choice format

## License

This is an educational tool for studying Finnish Amateur Radio exams.

Question translations and materials are based on official Finnish amateur radio examination materials.

## Notes

- The K-module translation is unofficial
- Some terminology may differ from official examination materials
- For official information, visit: https://www.sral.fi/

## Development

### Technologies Used
- Pure HTML/CSS/JavaScript (no frameworks required)
- Python for question parsing
- Responsive design for mobile and desktop

### Future Improvements
- Track progress across sessions (localStorage)
- Category-specific practice
- Timed exam mode
- Statistics and performance tracking
- Bookmarking difficult questions