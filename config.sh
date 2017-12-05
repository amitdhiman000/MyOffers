#! /bin/bash

help()
{
	echo "USAGE : "
	echo ""
	echo "config.sh migrate"
	echo ""
	echo "config.sh unmigrate"
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
}

if [[ $1 == "migrate" ]]
then
	migrate
elif [[ $1 == "unmigrate" ]]
then
	unmigrate
else
	help
fi
