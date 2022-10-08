python manage.py makemigrations users --no-input
python manage.py makemigrations food_app --no-input
python manage.py migrate --no-input
python manage.py import_data --no-input