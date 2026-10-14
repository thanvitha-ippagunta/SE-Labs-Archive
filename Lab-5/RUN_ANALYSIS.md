# Lab 5 - Commands to verify and generate the three report files

Use these commands in the **repository folder** on Windows PowerShell. The source file in this assigned project is `parking_system.py`, even though the generic handout uses `inventory_system.py` in its examples.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe parking_system.py
```

When the program asks for a plate, press Enter to skip the optional revoke action.

Then run all three analysis tools:

```powershell
.\.venv\Scripts\python.exe -m pylint parking_system.py > pylint_report.txt
.\.venv\Scripts\python.exe -m bandit -r parking_system.py > bandit_report.txt
.\.venv\Scripts\python.exe -m flake8 parking_system.py > flake8_report.txt
```

Open the reports using:

```powershell
Get-Content pylint_report.txt
Get-Content bandit_report.txt
Get-Content flake8_report.txt
```

An empty `flake8_report.txt` normally means no Flake8 findings. Read the Pylint score at the end of its report; the repo asks you to aim above 9.5. A successful Bandit scan typically prints a summary containing `No issues identified`.

The lab handout asks you to compare findings from before and after the fixes. If you need original/baseline reports as evidence, generate those by running the tools on the **original file** before replacing it (or check out the original version temporarily in a separate folder). Label the reports clearly as `before` or `after`; never present post-fix output as baseline evidence.

**What to commit:** `parking_system.py`, `issues.md`, `reflection.md`, `tests/test_parking_system.py`, `requirements-dev.txt`, `RUN_ANALYSIS.md`, and the three report `.txt` files **after generating them**. Do not commit `.venv`, `__pycache__`, or the generated `permits.json` database.
