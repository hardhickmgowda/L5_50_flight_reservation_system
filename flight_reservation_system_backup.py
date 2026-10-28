"""Simple flight reservation and passenger manifest manager."""

import hashlib
import json
import secrets
from pathlib import Path


FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

TOTAL_REVENUE = 0.0


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book one available seat and append a baggage log entry if requested."""
    global TOTAL_REVENUE
    if baggage_tags is None:
        baggage_tags = []

    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["is_full"] or flight["seats"] <= 0:
        return False

    flight["seats"] -= 1
    flight["is_full"] = flight["seats"] == 0
    TOTAL_REVENUE += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel a flight booking by restoring one seat for a known flight."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        return False
    flight["seats"] += 1
    flight["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return whether a known flight has at least one available seat."""
    flight = FLIGHTS.get(flight_no)
    return flight is not None and not flight["is_full"] and flight["seats"] > 0


def calculate_baggage_fee(flight_no, surcharge_rate):
    """Calculate a baggage surcharge using a numeric rate from 0 to 1."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        raise ValueError(f"Unknown flight: {flight_no}")
    if (
        not isinstance(surcharge_rate, (int, float))
        or not 0 <= surcharge_rate <= 1
    ):
        raise ValueError("surcharge_rate must be a number between 0 and 1")
    return flight["fare"] * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 digest for a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit cryptographically secure boarding PIN."""
    return f"{secrets.randbelow(9000) + 1000}"


def export_flight_manifest(filename="flight_manifest.json"):
    """Export flight data as JSON to the requested file."""
    output_path = Path(filename)
    output_path.write_text(json.dumps(FLIGHTS, indent=2), encoding="utf-8")
    print(f"Boarding manifest exported to: {output_path}")


def get_flight_summary(flight_data):
    """Count flights that currently have available seats."""
    return sum(
        1 for details in flight_data.values()
        if not details["is_full"] and details["seats"] > 0
    )


def main():
    """Run a small demonstration of the reservation operations."""
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))


if __name__ == "__main__":
    main()
