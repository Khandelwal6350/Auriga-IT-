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
        raw_price = row.get("price")
        display_name, class_key = _normalise_class_name(raw_name)

        if not display_name:
            rejected.append({
                "seat_class": "<missing>",
                "raw_seat_class": raw_name,
                "raw_price": raw_price,
                "reason": "seat_class is blank",
            })
            continue

        try:
            price = _parse_price(raw_price)
        except (TypeError, ValueError) as exc:
            rejected.append({
                "seat_class": display_name,
                "raw_seat_class": raw_name,
                "raw_price": raw_price,
                "reason": str(exc),
            })
            continue
        valid_rows.append((class_key, display_name, price, raw_name, raw_price))

    deduplicated = []
    for class_key, display_name, price, raw_name, raw_price in valid_rows:
        previous = imported_by_key.get(class_key)
        if previous is not None:
            deduplicated.append({
                "seat_class": previous["seat_class"],
                "price": previous["price"],
                "raw_seat_class": previous["raw_seat_class"],
                "raw_price": previous["raw_price"],
                "reason": "duplicate seat class; replaced by the last valid record",
            })
        imported_by_key[class_key] = {
            "seat_class": display_name,
            "price": price,
            "raw_seat_class": raw_name,
            "raw_price": raw_price,
        }

    return {
        "imported": [
            {"seat_class": item["seat_class"], "price": item["price"]}
            for item in imported_by_key.values()
        ],
        "deduplicated": deduplicated,
        "rejected": rejected,
    }


def import_price_list_from_csv(path: str) -> dict:
    """Read a seat-class price CSV and clean its rows."""
    with open(path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, restkey="__extra_columns__")
        if reader.fieldnames is None or {"seat_class", "price"} - set(reader.fieldnames):
            raise ValueError("CSV must contain seat_class and price columns")

        clean_rows = []
        malformed_rows = []
        for row_number, row in enumerate(reader, start=2):
            extra_columns = row.pop("__extra_columns__", None)
            if extra_columns:
                malformed_rows.append({
                    "seat_class": row.get("seat_class") or "<missing>",
                    "raw_seat_class": row.get("seat_class"),
                    "raw_price": row.get("price"),
                    "reason": f"row {row_number} contains extra columns",
                })
            else:
                clean_rows.append(row)

        result = clean_price_list(clean_rows)
        result["rejected"] = malformed_rows + result["rejected"]
        return result
