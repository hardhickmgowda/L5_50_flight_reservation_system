@echo off
REM Run from the folder containing flight_reservation_system.py
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install pylint bandit flake8
python flight_reservation_system.py
pylint flight_reservation_system.py > pylint_report_after.txt
bandit -r flight_reservation_system.py > bandit_report_after.txt
flake8 flight_reservation_system.py > flake8_report_after.txt
echo Reports saved. Review them before submission.
