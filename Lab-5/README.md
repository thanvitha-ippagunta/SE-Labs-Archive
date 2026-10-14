# Lab 5: Static Code Analysis — Campus Parking Permit Manager

## Project overview

This repository contains the completed Lab 5 static code analysis assignment for a Python-based Campus Parking Permit Manager. The program registers vehicle permits for parking zones **A, B, and C**, revokes permits, checks expiry dates, flags vehicles without valid permission for a zone, and saves permit records to a JSON file.

The goal of the lab was to inspect the starter program with **Pylint**, **Bandit**, and **Flake8**, fix at least four identified issues, and document the corrections. The updated version addresses **13 issues** recorded in [`issues.md`](issues.md).

## Main corrections

- Replaced the shared mutable default list with `None` to prevent data from leaking between calls.
- Replaced bare `except:` blocks with specific exception handling.
- Used `secrets.randbelow()` instead of predictable pseudo-random permit IDs, with collision checking.
- Added validation for vehicle plates, parking zones, permit expiry dates, and stored JSON records.
- Corrected expiry-date comparisons so a permit remains valid through its stated expiry date.
- Improved file handling and error reporting when loading or saving permit data.
- Avoided resetting an existing permit when the same vehicle is registered again.
- Added a `main()` entry-point guard, clearer naming, docstrings, and logging.

See [`issues.md`](issues.md) for the full issue table, original line references, priority, and fix details.

## Verification results

The following results were obtained after making the changes:

| Verification | Result |
| --- | --- |
| Pylint | **10.00 / 10** |
| Bandit | **0 issues identified** |
| Flake8 | **No violations reported** |
| Unit tests | **13 tests passed** |

The tool results are saved in [`pylint_report.txt`](pylint_report.txt), [`bandit_report.txt`](bandit_report.txt), and [`flake8_report.txt`](flake8_report.txt). The empty Flake8 report indicates no reported violations. Automated test output is also available in [`unit_test_results.txt`](unit_test_results.txt).

These results are checks on the tested version of the program; they do not guarantee the absence of every possible bug.

## Setup and run (Windows PowerShell)

Open PowerShell in the **`L5_10_parking_permits` repository folder** and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe parking_system.py
```

When prompted for a plate to revoke, press **Enter** to skip the optional revocation.

The program stores permits in `permits.json` when run. This is generated application data and is excluded from version control.

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Re-run static analysis

```powershell
.\.venv\Scripts\python.exe -m pylint parking_system.py > pylint_report.txt
.\.venv\Scripts\python.exe -m bandit -r parking_system.py > bandit_report.txt
.\.venv\Scripts\python.exe -m flake8 parking_system.py > flake8_report.txt
```

View the reports:

```powershell
Get-Content pylint_report.txt
Get-Content bandit_report.txt
Get-Content flake8_report.txt
```

For additional verification guidance, see [`RUN_ANALYSIS.md`](RUN_ANALYSIS.md).

## Submission files

| File / folder | Purpose |
| --- | --- |
| `parking_system.py` | Updated parking permit manager |
| `issues.md` | Filled-out table of 13 issues and how they were fixed |
| `reflection.md` | Four reflection answers based on the lab objectives |
| `pylint_report.txt` | Final Pylint output |
| `bandit_report.txt` | Final Bandit output |
| `flake8_report.txt` | Final Flake8 output |
| `tests/` | Regression tests |
| `unit_test_results.txt` | Recorded test output |
| `requirements-dev.txt` | Static analysis tool dependencies |
| `RUN_ANALYSIS.md` | Additional setup and analysis instructions |

## Assignment reference

Original starter repository: [SETAPESU26/L5_10_parking_permits](https://github.com/SETAPESU26/L5_10_parking_permits).

The Lab 5 handout requires an updated Python program with at least four issues fixed, a completed issue table, and reflection answers. This repository includes those deliverables along with tool reports and regression tests.

**Reflection note:** The provided handout references reflection questions but does not show their exact wording. The answers in `reflection.md` address the stated lab learning outcomes; they should be adjusted if the instructor supplies different questions.
