"""Campus parking permit manager with validated, persisted registrations."""

import json
import logging
import secrets
from datetime import date, timedelta
from pathlib import Path

LOGGER = logging.getLogger(__name__)
ZONES = frozenset({"A", "B", "C"})
PERMIT_VALIDITY_DAYS = 180
DEFAULT_DATABASE = "permits.json"

permits: dict[str, dict[str, str]] = {}


def normalize_plate(vehicle_plate: str) -> str:
    """Return uppercase nonempty plate text, rejecting invalid input."""
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        raise ValueError("Vehicle plate must be a nonempty string.")
    return vehicle_plate.strip().upper()


def register_permit(
    vehicle_plate: str,
    zone_id: str,
    zone_records: list[tuple[str, str]] | None = None,
) -> str | None:
    """Register a valid plate and zone, or return None if invalid."""
    try:
        plate = normalize_plate(vehicle_plate)
    except ValueError as error:
        LOGGER.warning("Registration rejected: %s", error)
        return None

    if not isinstance(zone_id, str) or zone_id.strip().upper() not in ZONES:
        LOGGER.warning("Registration rejected: invalid zone %r", zone_id)
        return None
    zone = zone_id.strip().upper()
    if zone_records is not None and not isinstance(zone_records, list):
        raise TypeError("zone_records must be a list or None")
    if plate in permits:
        LOGGER.info("Retaining existing permit for %s", plate)
        return permits[plate]["permit"]

    # Secrets avoids the predictable pseudo-random permit IDs in the starter.
    existing_ids = {record["permit"] for record in permits.values()}
    if len(existing_ids) >= 90_000:
        raise RuntimeError("All possible permit numbers are allocated.")
    permit_no = f"P{secrets.randbelow(90_000) + 10_000}"
    while permit_no in existing_ids:
        permit_no = f"P{secrets.randbelow(90_000) + 10_000}"

    expiry = date.today() + timedelta(days=PERMIT_VALIDITY_DAYS)
    permits[plate] = {
        "zone": zone,
        "permit": permit_no,
        "expiry": expiry.isoformat(),
    }
    if zone_records is not None:
        zone_records.append((plate, zone))
    return permit_no


def revoke_permit(vehicle_plate: str) -> bool:
    """Remove an existing permit, returning whether a removal occurred."""
    try:
        plate = normalize_plate(vehicle_plate)
    except ValueError:
        return False
    return permits.pop(plate, None) is not None


def is_expired(vehicle_plate: str) -> bool:
    """Treat missing or incorrectly formatted permits as expired."""
    try:
        expiry_text = permits[normalize_plate(vehicle_plate)]["expiry"]
        expiry = date.fromisoformat(expiry_text)
    except (KeyError, TypeError, ValueError):
        return True
    return expiry < date.today()


def scan_zone(zone_id: str, plates_seen: list[str]) -> list[str]:
    """Flag plates lacking a current permit for the selected zone."""
    if zone_id not in ZONES:
        raise ValueError(f"Unknown zone: {zone_id!r}")

    flagged = []
    for vehicle_plate in plates_seen:
        try:
            plate = normalize_plate(vehicle_plate)
        except ValueError:
            flagged.append(vehicle_plate)
            continue
        invalid_zone = plate in permits and permits[plate]["zone"] != zone_id
        if plate not in permits or invalid_zone or is_expired(plate):
            flagged.append(vehicle_plate)
    return flagged


def _valid_saved_record(vehicle_plate: str, record: object) -> bool:
    """Validate a loaded JSON permit before trusting its contents."""
    if (
        not isinstance(vehicle_plate, str)
        or not vehicle_plate.strip()
        or not isinstance(record, dict)
    ):
        return False
    zone = record.get("zone")
    if not isinstance(zone, str) or zone not in ZONES:
        return False
    permit_id = record.get("permit")
    if (
        not isinstance(permit_id, str)
        or len(permit_id) != 6
        or not permit_id.startswith("P")
        or not permit_id[1:].isdigit()
    ):
        return False
    expiry = record.get("expiry")
    if not isinstance(expiry, str):
        return False
    try:
        parsed_date = date.fromisoformat(expiry)
    except ValueError:
        return False
    return parsed_date.isoformat() == expiry


def load_permit_database(file: str | Path = DEFAULT_DATABASE) -> None:
    """Read the database, skipping invalid records and missing files."""
    try:
        with open(file, "r", encoding="utf-8") as database_file:
            saved_data = json.load(database_file)
    except FileNotFoundError:
        permits.clear()
        return
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError("Invalid JSON in permit database.") from error

    if not isinstance(saved_data, dict):
        raise ValueError("Permit database must be a JSON object.")

    valid_records: dict[str, dict[str, str]] = {}
    for plate, record in saved_data.items():
        if not _valid_saved_record(plate, record):
            LOGGER.warning("Skipping invalid saved permit for %r", plate)
            continue
        valid_records[normalize_plate(plate)] = {
            "zone": record["zone"],
            "permit": record["permit"],
            "expiry": record["expiry"],
        }
    permits.clear()
    permits.update(valid_records)


def save_permit_database(file: str | Path = DEFAULT_DATABASE) -> None:
    """Write the permit database using a managed, UTF-8 file handle."""
    with open(file, "w", encoding="utf-8") as database_file:
        json.dump(permits, database_file, indent=2, sort_keys=True)
        database_file.write("\n")


def set_expiry(vehicle_plate: str, date_text: str) -> None:
    """Set the expiry of an existing permit to an ISO YYYY-MM-DD date."""
    if not isinstance(date_text, str):
        raise ValueError("Expiry must use YYYY-MM-DD format.")
    try:
        expiry = date.fromisoformat(date_text)
    except ValueError as error:
        raise ValueError("Expiry must use YYYY-MM-DD format.") from error
    if expiry.isoformat() != date_text:
        raise ValueError("Expiry must use YYYY-MM-DD format.")
    permits[normalize_plate(vehicle_plate)]["expiry"] = expiry.isoformat()


def main() -> None:
    """Demonstrate registration, zone scanning, and optional revocation."""
    logging.basicConfig(
        level=logging.WARNING, format="%(levelname)s: %(message)s"
    )
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")  # Rejected: invalid zone.
    register_permit("", "B")  # Rejected: empty plate.
    register_permit(None, "C")  # Rejected: missing plate.
    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")
    seen = ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]
    print(f"Flagged in zone A: {scan_zone('A', seen)}")
    user_plate = input("Plate to revoke (Enter to skip): ").strip()
    if user_plate and not revoke_permit(user_plate):
        print("No permit found for that plate.")
    save_permit_database()
    print(f"Permits on file: {len(permits)}")


if __name__ == "__main__":
    main()
