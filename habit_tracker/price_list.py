"""Utilities for importing and cleaning seat-class price lists."""

import csv
import re


_PRICE_PATTERN = re.compile(r"^\s*(?:₹\s*)?([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:/-)?\s*$")


def _parse_price(raw_price):
    """Return a positive price as a float, or raise ValueError."""
    if raw_price is None or not str(raw_price).strip():
        raise ValueError("price is blank")

    if str(raw_price).strip().startswith("-"):
        raise ValueError("price cannot be negative")

    match = _PRICE_PATTERN.match(str(raw_price))
    if not match:
        raise ValueError("price is not a valid number")

    price = float(match.group(1).replace(",", ""))
    if price <= 0:
        raise ValueError("price must be positive")
    return price


def _normalise_class_name(raw_name):
    """Return a display name and a case-insensitive comparison key."""
    display_name = " ".join(str(raw_name or "").split()).title()
    return display_name, display_name.casefold()


def clean_price_list(raw_rows: list[dict]) -> dict:
    """Clean seat-class price rows and report imported, duplicate, and rejected data."""
    imported_by_key = {}
    rejected = []
    valid_rows = []

    for row in raw_rows:
        raw_name = row.get("seat_class", "")
        display_name, class_key = _normalise_class_name(raw_name)
        try:
            price = _parse_price(row.get("price"))
        except (TypeError, ValueError) as exc:
            rejected.append({"seat_class": display_name or str(raw_name), "reason": str(exc)})
            continue
        valid_rows.append((class_key, display_name, price))

    deduplicated = []
    for class_key, display_name, price in valid_rows:
        previous = imported_by_key.get(class_key)
        if previous is not None:
            deduplicated.append({
                "seat_class": previous["seat_class"],
                "price": previous["price"],
                "reason": "duplicate seat class; replaced by the last valid record",
            })
        imported_by_key[class_key] = {"seat_class": display_name, "price": price}

    return {
        "imported": list(imported_by_key.values()),
        "deduplicated": deduplicated,
        "rejected": rejected,
    }


def import_price_list_from_csv(path: str) -> dict:
    """Read a seat-class price CSV and clean its rows."""
    with open(path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None or {"seat_class", "price"} - set(reader.fieldnames):
            raise ValueError("CSV must contain seat_class and price columns")
        return clean_price_list(list(reader))
