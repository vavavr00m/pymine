IP_ADDRESS=127.0.0.1
IP_PORT=9862
IP_TUPLE=$(IP_ADDRESS):$(IP_PORT)

all: client

clean:
	-rm `find . -name "*~"`
	-rm `find . -name "*.pyc"`
	-rm `find . -name "*.tmp"`

clobber: clean
	rm database/*/sqlite3.db
	rm -r database/*/files/

perms:
	chmod 644 `find . -type f`
	chmod 755 `find . -type d`
	chmod 755 `find . -name "*.py"`
	chmod 755 `find . -name "*.pl"`
	chmod 755 `find . -name "*.sh"`

##################################################################

client:
	open http://$(IP_TUPLE)/

server:
	python manage.py runserver $(IP_TUPLE)

##################################################################

start:
	python manage.py startapp api

shell:
	python manage.py shell

dbtest:
	python manage.py validate
	python manage.py sqlall api

dbsync: dbtest
	python manage.py syncdb --noinput --traceback

dbclean:
	python manage.py cleanup

dbdump:
	@python manage.py dumpdata

##################################################################

syntax:
	find */ -name "*.py" | while read f ; do echo $$f ; python $$f ; echo "" ; done

# :-)
alecm:
	env MINE_EMAIL=alec.muffett@gmail.com ./runme-setup.sh
	make server
