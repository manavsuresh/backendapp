pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic
yes
py manage.py runserver