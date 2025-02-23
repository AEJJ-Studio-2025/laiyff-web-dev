cd ../
source env/bin/activate

python manage.py makemigrations
python manage.py migrate --fake
python manage.py migrate
