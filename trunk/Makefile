IP_ADDRESS=127.0.0.1
IP_PORT=9862
IP_TUPLE=$(IP_ADDRESS):$(IP_PORT)

client:
	open http://$(IP_TUPLE)/

server:
	python manage.py runserver $(IP_TUPLE)

start:
	python manage.py startapp frontend

clean:
	-rm `find . -name "*~"`
	-rm `find . -name "*.pyc"`

test:
	python manage.py validate 
	python manage.py sqlall frontend

sync: test
	python manage.py syncdb

clobber: clean
	rm database/*sqlite3.db

shell:
	python manage.py shell

perms:
	chmod 644 `find . -type f`
	chmod 755 `find . -type d`
	chmod 755 `find . -name "*.p[yl]"`
