Setting Up Your Environment
-----------------------------------------------------------------------

- Install [pip]
- Install [virtualenv]

From the api directory run:
	
	mkvirtualenv whoseopinion
	pip install django #(1.7)
	pip install djangorestframework
	python manage.py migrate
	python manage.py syncdb


[pip]:http://pip.readthedocs.org/en/latest/installing.html
[virtualenv]:http://virtualenv.readthedocs.org/en/latest/virtualenv.html

