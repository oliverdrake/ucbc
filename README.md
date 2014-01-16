UC Brew Club
============

Website for the UC brew club, pull requests welcome :)

Development Setup
-----------------

Install python 3.2, pip and sqlite for your platform

pip install -r prod-requirements.txt  
pip install -r dev-requirements.txt

Create a new file called secret.py in ucbc/settings, populate it with:
 - EMAIL_HOST_PASSWORD
 - SECRET_KEY

Run ./migrate.sh (or syncdb followed by south stuff)  
Run ./manage.py collectstatic

Now you should be able to run the dev server: ./manage.py runserver.


Release Notes
-------------

See https://github.com/oliverdrake/ucbc/issues/milestones



