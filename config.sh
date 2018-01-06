#! /bin/bash

help()
{
	echo "USAGE : "
	echo ""
	echo "config.sh migrate"
	echo ""
	echo "config.sh unmigrate"
	echo ""
	echo "config.sh preload"
}

migrate()
{
	python manage.py makemigrations
	python manage.py migrate
}

unmigrate()
{
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	rm -f devel.sqlite3
}

preload()
{
	python manage.py preload
}

if [[ $1 == "migrate" ]]
then
	migrate
elif [[ $1 == "unmigrate" ]]
then
	unmigrate
elif [[ $1 == "preload" ]]
then
	preload
else
	help
fi
