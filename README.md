# DocSage - Skin Disease Diagnosis Platform

## Project Overview

DocSage is a comprehensive web application designed to help diagnose and manage skin diseases using advanced machine learning techniques. This final year project aims to bridge the gap between patients and healthcare professionals by providing an innovative platform for skin disease diagnosis and medical consultation.

## Key Features

- 🩺 ML-powered Skin Disease Diagnosis
- 🔍 Doctor Search and Booking System
- 📝 Health Articles Management
- 💬 Direct Messaging Between Patients and Doctors
- 👤 Comprehensive User and Doctor Profile Management

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Machine Learning**: Custom Skin Disease Diagnosis Model
- **Database**: SQLite (Development), PostgreSQL/MySQL (Production)

## Prerequisites

- Python 3.9+
- pip
- virtualenv

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/UsamaTech21/DocSage.git
cd DocSage
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Project Structure
```
docsage/
├── articles/            # Articles management app
├── doctors/             # Doctors-related functionality
├── users/               # User authentication and profiles
├── symptom_checker/     # Machine Learning model integration
├── templates/           # HTML templates
└── static/              # Static files (CSS, JS, images)
```

## Machine Learning Model

The core of DocSage is its custom-trained machine learning model for skin disease diagnosis. The model analyzes uploaded images to provide preliminary medical insights.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more details.

## Contact

Project Link: [https://github.com/UsamaTech21/DocSage](https://github.com/UsamaTech21/DocSage)

## Acknowledgments

- Final Year Project
- Supervised by [Supervisor Name]
- Developed with ❤️ by [Your Name/Team Name] 
