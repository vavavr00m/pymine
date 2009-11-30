# configurables
MY_EMAIL=email.address@mydomain.dom
IP_ADDRESS_AND_PORT=127.0.0.1:9862

# external code
PYDOC=pydoc

##################################################################

all:
	@echo ""
	@echo make setup - configures the installation
	@echo make server - launches the server
	@echo make client - opens a client on $(IP_ADDRESS_AND_PORT)
	@echo make clean - removes cruft files
	@echo make clobber - clean, and removes database files
	@echo make perms - sets sane unix permissions on the installation
	@echo make hard-reset - automated nuke-and-rebuild for developers
	@echo ""

clean:
	-rm `find . -name "*~"`
	-rm `find . -name "*.pyc"`
	-rm `find . -name "*.tmp"`

clobber: clean
	-rm -r database/*
	-rm etc/cookies.txt
	-rm settings.py

perms:
	chmod 755 `find . -type d`
	chmod 644 `find . -type f`
	chmod -R go-rwx etc/
	chmod 755 `find . -name "*.py"`
	chmod 755 `find . -name "*.pl"`
	chmod 755 `find . -name "*.sh"`

setup:
	sh mine-setup.sh
	make perms

hard-reset: clobber # brute-force rebuild from scratch
	env MINE_USER_EMAIL=$(MY_EMAIL) make setup
	make server

##################################################################

client:
	@echo trying to open http://$(IP_ADDRESS_AND_PORT)/
	-test -x /usr/bin/gnome-open && gnome-open http://$(IP_ADDRESS_AND_PORT)/
	-test -d /System/Library && open http://$(IP_ADDRESS_AND_PORT)/

server:
	python manage.py runserver $(IP_ADDRESS_AND_PORT)

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

docs:
	( cd public_html ; pydoctor --add-package=../../pymine --project-name="pymine" --make-html )
	( cd public_html/apidocs ; perl -pi~ -e "s/2009-\d{1,2}-\d{1,2} \d\d:\d\d:\d\d/(date elided)/go" *.html )
	( cd public_html/apidocs ; rm *~ )
