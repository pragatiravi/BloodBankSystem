@echo off
echo Setting up Blood Bank System on Windows...

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r BloodBankSystem\BloodBankSystem\requirements.txt

REM Create .env file if it doesn't exist
if not exist BloodBankSystem\BloodBankSystem\.env (
    echo Creating .env file...
    copy BloodBankSystem\BloodBankSystem\.env.example BloodBankSystem\BloodBankSystem\.env
)

REM Run migrations
echo Running database migrations...
python BloodBankSystem\BloodBankSystem\manage.py migrate

echo.
echo Setup complete! You can now:
echo 1. Create a superuser: python BloodBankSystem\BloodBankSystem\manage.py createsuperuser
echo 2. Run the server: python BloodBankSystem\BloodBankSystem\manage.py runserver
echo.
echo The application will be available at http://127.0.0.1:8000/

pause
