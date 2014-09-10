from __future__ import with_statement
from fabric.api import *

def shell():
	local('python manage.py shell')

def runserver():
	local('python manage.py runserver')

def test():
	local('python manage.py test')

def lint():
	local('flake8 questions')

def make_requirements():
	local('pip freeze -l > requirements.txt')

