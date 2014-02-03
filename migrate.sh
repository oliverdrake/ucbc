#!/bin/bash

./manage.py syncdb
#./manage.py schemamigration orders --initial
#./manage.py schemamigration orders --fake
#./manage.py schemamigration inventory --auto
./manage.py schemamigration orders --auto
./manage.py schemamigration main --auto
#./manage.py migrate --fake
./manage.py migrate
