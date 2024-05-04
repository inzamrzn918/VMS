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

## ENDPOINTS
```
| Endpoint                                  | Method | Description                 |
|-------------------------------------------|--------|-----------------------------|
| /vendors                                  | GET    | Retrieve all vendors        |
| /vendors/{vendor_id}                      | GET    | Retrieve single vendor      |
| /vendors                                  | POST   | Create Vendor               |
| /vendors/{vendor_id}                      | PUT    | Update Vendor               |
| /vendors/{vendor_id}                      | DELETE | Delete Vendor               |
| /vendors/{vendor_id}/performance          | GET    | Retrieve vendor performance |
|                                           | POST   | Update vendor performance   |
|                                           | DELETE | Delete vendor performance   |
| /purchase_orders                          | GET    | Retrieve all orders         |
| /purchase_orders/{po_id}                  | GET    | Retrieve single order       |
| /purchase_orders                          | POST   | Create Order                |
| /purchase_orders/{po_id}                  | PUT    | Update Order                |
| /purchase_orders/{po_id}                  | DELETE | Delete Order                |
| /purchase_orders/{po_id}/acknowledge      | POST   | Acknowledge the order       |

```