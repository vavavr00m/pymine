# configurables
MY_EMAIL=email.address@mydomain.dom
IP_ADDRESS_AND_PORT=127.0.0.1:9862

# external code
PYDOC=pydoc

# production lockfile
SAFELOCK=".this_mine_is_being_used"

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

safe:
	date > $(SAFELOCK)
	chmod 400 $(SAFELOCK)

unsafe:
	-@test -f $(SAFELOCK) && echo to make unsafe, remove file: $(SAFELOCK)

clean:
	-rm `find . -name "*~"`
	-rm `find . -name "*.tmp"`
	-rm etc/cookies.txt
	-rm etc/cookies2.txt

clobber: clean
	if [ -f $(SAFELOCK) ] ; then exit 1 ; fi
	-rm settings.py
	-rm -r database/*
	-rm `find . -name "*.pyc"`

perms:
	chmod 755 `find . -type d`
	chmod 644 `find . -type f`
	chmod -R go-rwx etc/
	chmod 755 `find . -name "*.py"`
	chmod 755 `find . -name "*.pl"`
	chmod 755 `find . -name "*.sh"`
	chmod 755 miner

setup:
	if [ -f $(SAFELOCK) ] ; then exit 1 ; fi
	sh tools/minesetup.sh
	make perms

hard-reset: clobber # brute-force rebuild from scratch
	if [ -f $(SAFELOCK) ] ; then exit 1 ; fi
	env MINE_USER_EMAIL=$(MY_EMAIL) make setup
	make server

##################################################################


# THESE ARE PROBABLY THE TWO THINGS YOU NEED TO USE

client:
	@echo trying to open http://$(IP_ADDRESS_AND_PORT)/
	-test -x /usr/bin/gnome-open && gnome-open http://$(IP_ADDRESS_AND_PORT)/
	-test -d /System/Library && open http://$(IP_ADDRESS_AND_PORT)/

server:
	python manage.py runserver $(IP_ADDRESS_AND_PORT)

##################################################################

shell:
	python manage.py shell

dbtest:
	python manage.py validate
	python manage.py sqlall api

dbsync:
	python manage.py syncdb --noinput --traceback

dbclean:
	python manage.py cleanup

dbdump:
	@python manage.py dumpdata

##################################################################

docs:
	( cd public_html ; pydoctor --add-package=../../pymine --project-name="pymine" --make-html )
	( cd public_html/apidocs ; perl -pi~ -e "s/201\d-\d{1,2}-\d{1,2} \d\d:\d\d:\d\d/(date elided)/go" *.html )
	( cd public_html/apidocs ; rm *~ )
	@echo DID YOU REMEMBER TO DO 'make clobber' FIRST?
