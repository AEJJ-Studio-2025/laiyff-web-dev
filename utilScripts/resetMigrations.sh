cd ../
source env/bin/activate

# python manage.py migrate --fake wagtailmenus zero
python manage.py migrate --fake home zero
