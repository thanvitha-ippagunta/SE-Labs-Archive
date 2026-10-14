# Lab 5 - Static Code Analysis: Issue Table

**Assigned application:** Campus Parking Permit Manager (`parking_system.py`)  
**Original source:** `SETAPESU26/L5_10_parking_permits`, `main` branch  
**Line numbers below refer to the ORIGINAL starter file (not the updated file).**  
**Prioritization:** Security and functional correctness first, followed by code quality and style.

| Issue | Type / priority | Original line(s) | Description | Fix approach and verification |
|---|---|---|---|---|
| Predictable permit IDs (`random.randint`; Bandit B311) | Security / medium | 2, 9 | The starter uses a predictable pseudo-random number generator for permit IDs. | Replaced with `secrets.randbelow`; also checks for an existing ID before assigning it. |
| Broad `except:` clauses (Flake8 E722; Pylint bare-except) | Bug / high | 14-15, 19-20, 26-27, 39-40 | Suppress unrelated failures, including malformed records, and make errors difficult to diagnose. | Removed blanket catches; handle specific `ValueError`, `KeyError`, `TypeError`, `FileNotFoundError`, `JSONDecodeError`, and `UnicodeError` as appropriate. |
| Expired permit may be accepted after invalid date | Security / high | 23-27, 55 | `setExpiry` stores `01/01/2020`, but `is_expired` expects `%Y-%m-%d`; its broad exception then returns `False`, treating the bad date as not expired. | Reject malformed date updates; treat missing or malformed expiry as expired; use `2020-01-01` in the demo. |
| Missing vehicle plate and zone validation | Correctness / high | 7-12, 52-54 | Original code accepts `None`, an empty plate and zone `Z`, even though only A-C are supported. | Validate plate and zone before registering; normalize valid plate/zone text; return `None` for invalid registration. |
| Mutable default argument (`zone_records=[]`; Pylint W0102) | Bug / medium | 7, 12 | The same list survives across calls and can leak earlier registrations. | Changed default to `None` and append only to an explicitly supplied list. |
| Incorrect date comparison at midnight | Logic / medium | 24-25 | `datetime.strptime` creates midnight; comparing with `datetime.now()` marks permits expiring *today* as expired later that day. | Compare `date` objects instead; an expiry equal to today remains valid through that date. |
| Non-context-managed database read/write (Pylint R1732) | Resource management / medium | 38, 43-45 | `open()` is not used inside `with`, increasing the risk of leaked handles if parsing/writing fails. | Use `with open(..., encoding="utf-8")` for both loading and saving. |
| File read errors silently discard data | Data integrity / medium | 35-40 | Every read error sets all permits to `{}`, so the next save can overwrite valid data. | Treat a missing file as an empty registry; raise on malformed JSON rather than silently overwriting the stored database. |
| Unvalidated saved JSON records | Correctness / medium | 38 | Unknown zones, missing keys and bad dates are loaded as if trustworthy. | Validate each saved permit record and skip invalid entries with a warning. |
| Existing permit overwritten on repeated registration | Logic / medium | 11 | Registering the same plate again silently resets its zone and expiry. | Keep the existing permit and its original expiry for repeated registration attempts. |
| Unhandled invalid zone scanning | Correctness / low | 29-34 | A scan can be requested for a zone the application does not support. | Raise `ValueError` if the requested scan zone is not A, B or C. |
| Non-PEP8 name and missing docstrings / formatting | Style / low | 47, plus several function declarations and long statements | `setExpiry` is not snake_case; functions lack docstrings; some lines are long. | Renamed to `set_expiry`; added descriptions, standard formatting and f-strings in user-visible output. |
| Program executes when imported | Testability / medium | 63 | The original `main()` executes even when another module imports this file. | Added the `if __name__ == "__main__": main()` entry-point guard. |

## Verification

- **Executed:** `python -m py_compile parking_system.py` - passed.
- **Executed:** `python -m unittest discover -s tests -v` - 13 tests passed.
- **Required local verification:** Run Pylint, Bandit and Flake8 with the commands in `RUN_ANALYSIS.md`. Their exact scores and outputs are not claimed here because these third-party tools were unavailable in the preparation environment.
- **Expected behavior checked by unit tests:** input validation, duplicate registration, isolated list defaults, expiry handling, zone scanning, revocation, JSON round-trip, malformed records and missing database handling.

**Notes:** Bandit rates `B311` as low severity in some versions/settings; it is prioritized here as a security-related weakness in ID generation, not represented as a confirmed high-severity Bandit finding. Some functional problems are found by inspecting runtime behavior rather than the three static analysis tools alone.
