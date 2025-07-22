# DocSage - Skin Disease Diagnosis Platform

## Project Overview

DocSage is a comprehensive web application for skin disease diagnosis and medical consultation, leveraging machine learning to provide advanced healthcare solutions.

## Features

- ML-powered skin disease diagnosis
- Doctor search and booking system
- Health articles management
- Direct messaging between patients and doctors
- User and doctor profile management

## Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/UsamaTech21/DocSage.git
cd DocSage/docsage
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

## Environment Configuration

- Create a `.env` file in the project root for sensitive configurations
- Add the following sample configurations:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## Deployment Considerations

- Use PostgreSQL for production
- Set `DEBUG=False` in production
- Configure static and media file serving
- Set up proper security settings

## Machine Learning Model

The skin disease diagnosis uses a custom-trained ML model. Ensure you have the necessary dependencies installed.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Usama Tech - [GitHub Profile](https://github.com/UsamaTech21)
Project Link: [https://github.com/UsamaTech21/DocSage](https://github.com/UsamaTech21/DocSage)