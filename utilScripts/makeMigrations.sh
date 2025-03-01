cd ../
source env/bin/activate

# python manage.py migrate --fake wagtailmenus zero

python manage.py makemigrations
python manage.py migrate
