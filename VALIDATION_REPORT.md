# Ham Radio Question Database Validation Report

**Date:** 2025-11-04
**Status:** 3 Critical Issues Found

## Summary

- **K-module:** 245 questions parsed successfully ✓
- **T1-module:** 485 questions parsed successfully ✓
- **JSON files:** Generated successfully ✓
- **Critical issues:** 3 questions with no correct answers marked

## Fixed Issues

### 1. Em-dash formatting (T1-module) ✓ FIXED

**Issue:** 35 instances of em-dash (–) instead of regular hyphen (-)
**Location:** T1_kaikki_kysymykset_v3.txt
**Impact:** Parser couldn't recognize option lines properly
**Resolution:** Replaced all em-dashes with regular hyphens
**Backup:** T1_kaikki_kysymykset_v3.txt.backup_20251104_221728

## Critical Issues Requiring Manual Review

### Question 06016 (Line 2095)

```
06016 % Taajuutta 7 MHz vastaava amatöörialue on
06016A - 20 m
06016B - 15 m
06016C - 10 m
06016D - 80 m
```

**Problem:** All options marked incorrect (-)
**Expected:** One option should be marked correct (+)
**Note:** 7 MHz corresponds to the 40m band, but 40m is not listed in the options. The closest is 80m (option D, which is 3.5 MHz). This question may need correction from the official source.

### Question 06025 (Line 2143)

```
06025 % Aallonpituutta 15 m vastaava taajuusalue on
06025A - 7 MHz
06025B - 3,5 MHz
06025C - 14 MHz
06025D - 28 MHz
```

**Problem:** All options marked incorrect (-)
**Expected:** One option should be marked correct (+)
**Note:** 15m band is approximately 21 MHz, which is not in the options. 14 MHz (option C) is the 20m band, 28 MHz (option D) is the 10m band. This question may need correction from the official source.

### Question 10006 (Line 2822)

```
10006 % On totta, että
10006A - itsetehdyt radiolaitteet kuuluvat II-suojausluokkaan
10006B - käyttöjännitteen ollessa 12 V ei voi aiheutua palovaaraa
10006C - maadoitusvastuksen tulee olla mahdollisimman suuri
10006D - maadoituselektrodin liitosjohdon poikkipinta-ala saa olla 4 mm²
```

**Problem:** All options marked incorrect (-)
**Expected:** At least one option should be marked correct (+)
**Note:** This is a safety question. Requires verification against official question bank.

## Recommendations

1. **Compare with official question bank:** These 3 questions should be verified against the official Finnish amateur radio exam question bank

2. **Possible sources of error:**
   - OCR errors during PDF extraction
   - Manual transcription errors
   - Missing correct answer options

3. **Next steps:**
   - Locate the original question bank for questions 06016, 06025, and 10006
   - Verify correct answers
   - Update T1_kaikki_kysymykset_v3.txt
   - Re-run: `python3 parse_questions.py`

## Validation Commands

To re-validate after fixes:
```bash
python3 validate_questions.py
```

To regenerate JSON files:
```bash
python3 parse_questions.py
```

## Files Modified

- ✓ T1_kaikki_kysymykset_v3.txt (35 em-dashes fixed)
- ✓ k_questions.json (regenerated)
- ✓ t1_questions.json (regenerated)
- ✓ all_questions.json (regenerated)

## New Files Created

- validate_questions.py (validation script)
- fix_formatting.py (formatting fix script)
- T1_kaikki_kysymykset_v3.txt.backup_20251104_221728 (backup)
- VALIDATION_REPORT.md (this report)
