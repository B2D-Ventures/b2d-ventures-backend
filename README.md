# b2d-ventures-backend

```
python3 -m venv venv
source venv venv
python manage.py migrate
python manage.py loaddata db_dump.json # Ask J for the file.
python manage.py create_mock_deals # If you want to add the mockup data
python manage.py runserver
```