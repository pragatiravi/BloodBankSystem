# 🩸 Blood Bank Management System

A comprehensive web application for managing blood donations, requests, and donors. This system connects blood donors with people in need, streamlines the blood donation process, and helps save lives.


## ✨ Key Features

- **User Management**
  - Role-based access control (Admin, Donor, User)
  - Secure authentication and authorization
  - Profile management

- **Donor Management**
  - Donor registration and profile management
  - Blood group tracking and availability status
  - Donation history tracking

- **Blood Request System**
  - Blood request submission with patient details
  - Request tracking and status updates
  - Matching donors with compatible blood groups

- **Notification System**
  - Real-time notifications using WebSockets
  - Email alerts for critical requests
  - Status updates for donors and requesters

- **Admin Dashboard**
  - Comprehensive system management
  - User management and statistics
  - Blood inventory tracking

- **Cross-Platform Compatibility**
  - Works on Windows, macOS, and Linux
  - Responsive design for mobile and desktop
  - Environment-agnostic configuration
## ss of the web-app 
![image](https://github.com/user-attachments/assets/820872c8-342c-4eff-ab09-7cdfcd804ddc)
![image](https://github.com/user-attachments/assets/008efef4-e294-4925-b11e-f8947fd0b72c)
![image](https://github.com/user-attachments/assets/6d013051-68be-45b1-889a-6e7bc780f83b)
![image](https://github.com/user-attachments/assets/b4af5f5e-1b4f-42e9-bc2a-e7d1a923ed96)
![image](https://github.com/user-attachments/assets/7c26aa0c-a7a1-4239-8e7d-151639a24915)
![image](https://github.com/user-attachments/assets/345b781f-c4bf-4289-bd57-763463b4b702)
![image](https://github.com/user-attachments/assets/2fe9f1be-a4b0-4f91-9ff3-51e0a16f49c6)
![image](https://github.com/user-attachments/assets/567e34b0-bde7-4861-8bed-a450709da22e)
![image](https://github.com/user-attachments/assets/26259818-d57a-4a73-a1d3-2ee6c82c508f)
![image](https://github.com/user-attachments/assets/5bb035a9-9e17-4931-a8d4-72d99382b04f)
![image](https://github.com/user-attachments/assets/98374f9a-f191-41f0-b8b8-3e0942d60691)

## 🛠️ Technology Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 4
- **Database**: SQLite (default), PostgreSQL (optional)
- **Real-time Communication**: Django Channels
- **Form Handling**: Crispy Forms

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## 🚀 Installation

### Windows

```powershell
# Clone the repository
git clone https://github.com/pragatiravi/BloodBankSystem.git
cd BloodBankSystem

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r BloodBankSystem\BloodBankSystem\requirements.txt

# Set up environment variables
copy BloodBankSystem\BloodBankSystem\.env.example BloodBankSystem\BloodBankSystem\.env

# Run migrations
python BloodBankSystem\BloodBankSystem\manage.py migrate

# Create superuser (admin)
python BloodBankSystem\BloodBankSystem\manage.py createsuperuser

# Run the server
python BloodBankSystem\BloodBankSystem\manage.py runserver
```

### macOS/Linux

```bash
# Clone the repository
git clone https://github.com/pragatiravi/BloodBankSystem.git
cd BloodBankSystem

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r BloodBankSystem/BloodBankSystem/requirements.txt

# Set up environment variables
cp BloodBankSystem/BloodBankSystem/.env.example BloodBankSystem/BloodBankSystem/.env

# Run migrations
python BloodBankSystem/BloodBankSystem/manage.py migrate

# Create superuser (admin)
python BloodBankSystem/BloodBankSystem/manage.py createsuperuser

# Run the server
python BloodBankSystem/BloodBankSystem/manage.py runserver
```

## 🔧 Configuration

The application uses environment variables for configuration. Edit the `.env` file to customize:

### Database Configuration

#### SQLite (Default - Easiest for Local Development)

```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### PostgreSQL (For Production or Cross-System Access)

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bloodbank_db
DB_USER=bloodbank_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

## 👨‍💻 Usage

1. **Access the Application**
   - Open your browser and go to http://127.0.0.1:8000/
   - Log in with the superuser credentials you created

2. **Admin Dashboard**
   - Access the admin panel at http://127.0.0.1:8000/admin/
   - Manage users, donors, blood requests, and system settings

3. **User Roles**
   - **Admin**: Manage the entire system
   - **Donor**: Register as a donor, update availability, view matching requests
   - **User**: Submit blood requests, track request status, search for donors

## 📱 Application Workflow

1. **For Blood Requesters**
   - Register/Login to the system
   - Submit a blood request with patient and hospital details
   - Track the status of your request
   - Receive notifications when donors are available

2. **For Donors**
   - Register as a donor with your blood group and contact information
   - Update your availability status
   - View blood requests matching your blood group
   - Respond to requests and help save lives

3. **For Administrators**
   - Manage users, donors, and blood requests
   - Verify donor information
   - Handle blood request approvals
   - Generate reports and statistics

## 🌐 Cross-System Access

To make the system accessible from different machines:

1. Set up a centralized PostgreSQL database server
2. Configure all client systems to use the same database by updating their `.env` files
3. Ensure the database server is accessible from all client machines

## 🔒 Security Considerations

- Never expose your database directly to the internet
- Use a VPN or SSH tunnel for secure remote database access
- Keep your SECRET_KEY secure and different in production
- Set DEBUG=False in production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any questions or suggestions, please contact:
- GitHub: [pragatiravi](https://github.com/pragatiravi)

---

Made with ❤️ for blood donors and recipients everywhere.
