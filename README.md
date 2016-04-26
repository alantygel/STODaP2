# STODaP - Semantic Tags for Open Data Portals

Code of the Semantic Tags for Open Data Portals server. Stores tags, datasets, groups, global tags and global groups metadata.

## Dependencies
	sudo pip install Django==1.8
	pip install django-haystack
	sudo apt-get install python-mysqldb
	sudo apt-get install python-numpy
	sudo pip install scipy
	sudo pip install scikit-learn
	sudo pip install python-Levenshtein
	sudo pip install unidecode
	sudo pip install rdflib
	sudo pip install pycountry

## Install	
After copying the files, run the following commands to setup solr:

	python manage.py build_solr_schema
	python manage.py rebuild_index

And for running the server:
	python manage.py runserver [0.0.0.0:8000]
