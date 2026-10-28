#!/usr/bin/env bash
set -e
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pylint bandit flake8
python flight_reservation_system.py
pylint flight_reservation_system.py > pylint_report_after.txt || true
bandit -r flight_reservation_system.py > bandit_report_after.txt || true
flake8 flight_reservation_system.py > flake8_report_after.txt || true
echo "Reports saved. Review them before submission."
