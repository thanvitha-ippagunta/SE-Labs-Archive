# Lab 5 - Reflection: Static Code Analysis

**Note:** The supplied student handout says to answer reflection questions, and the repository README mentions *four* questions, but the actual wording of those four questions is absent from the supplied four-page handout. The following four answers address the lab objective and stated learning outcomes. If the instructor provides specific questions separately, replace these headings with the exact questions.

## 1. What is static code analysis, and why is it useful?

Static code analysis checks a program's source code without running the application. It helps detect unsafe patterns, style problems and potential bugs early. In this parking permit manager, the analysis highlighted practices such as bare `except:` blocks, a mutable default list and insecure random-number generation. Fixing these makes the program easier to maintain and reduces the chance of invalid permits being accepted.

## 2. How do Pylint, Flake8 and Bandit differ?

Pylint examines code quality and common programming mistakes, such as mutable defaults, naming conventions and missing docstrings. Flake8 focuses on style and straightforward programming errors, such as `E722` for a bare `except:` and long lines. Bandit checks for security-sensitive patterns; the original use of `random.randint` for an unpredictable-looking permit ID is an example of a `B311` concern. The tools complement one another rather than replacing one another.

## 3. Which issues were the most important to fix, and what did you change?

The most serious functional problem was expiry validation. The old code stored `01/01/2020`, but its parser expected `YYYY-MM-DD`. Because a broad exception returned `False`, the application could incorrectly treat that expired permit as valid. I changed the setter to validate dates, compared actual `date` objects and made malformed or missing permits fail closed. I also added plate and zone validation, replaced shared default lists, used `secrets` for permit IDs and made JSON file operations safer.

## 4. What did you learn from verifying the fixes?

A warning-free source file is not enough on its own: static analysis identifies suspicious code patterns, but it cannot prove the program behaves correctly. I added regression tests for valid and invalid registrations, expiry boundaries, revocation, zone scans and JSON storage. All 13 tests pass in the preparation environment. Running Pylint, Bandit and Flake8 again on the corrected file is still required to record the final tool-specific analysis results. This lab showed me why both static checks and behavior-based tests are useful before submitting code.
