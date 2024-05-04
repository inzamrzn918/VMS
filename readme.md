# VMS

Vendor Management System

## Installation

Clone Project 

```bash
git clone https://github.com/inzamrzn918/VMS.git
```
```bash
cd VMS
```

#### Install Packages
```
pip install -r requirements.txt
```
NB: Make sure to enable virtual environment


## Migration 
DEFAULT database is SQLite. To use another db please update following code in settings.py file
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
### Migration Commands

```bash
python manage.py makemigrations

python manage.py migrate
```

## Usage

```
 python manage.py runserver
```

ALL THE ENDPOINTS ARE PUBLIC AND AVAILABLE @ PORT 8000