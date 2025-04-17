#!/bin/bash
echo "Setting up Blood Bank System on macOS/Linux..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r BloodBankSystem/BloodBankSystem/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f "BloodBankSystem/BloodBankSystem/.env" ]; then
    echo "Creating .env file..."
    cp BloodBankSystem/BloodBankSystem/.env.example BloodBankSystem/BloodBankSystem/.env
fi

# Run migrations
echo "Running database migrations..."
python BloodBankSystem/BloodBankSystem/manage.py migrate

echo ""
echo "Setup complete! You can now:"
echo "1. Create a superuser: python BloodBankSystem/BloodBankSystem/manage.py createsuperuser"
echo "2. Run the server: python BloodBankSystem/BloodBankSystem/manage.py runserver"
echo ""
echo "The application will be available at http://127.0.0.1:8000/"
