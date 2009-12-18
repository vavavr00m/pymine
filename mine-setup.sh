#!/bin/sh

echo ""
echo setting up pymine in `pwd` via $0 $@
echo ""

DJANGO() {
    parent=`( cd .. ; pwd )` # horrible kludge but it saves typing
    env PYTHONPATH=$PYTHONPATH:$parent DJANGO_SETTINGS_MODULE=pymine.settings "$@"
}

PROMPT() {
    echo "$* \c"
}

YESNO() {
    while :
    do
	PROMPT "$@ ? (y/n)"

	read answer

	case "$answer" in
	    [Yy]*) return 0 ;;
	    [Nn]*) return 1 ;;
	    *) echo "please answer yes or no."
	esac
    done
}

DEFAULT_SUPERUSER=pickaxe
DEFAULT_USER=$USER

if [ $DEFAULT_USER = root ]
then
    DEFAULT_USER=pymine # anything but root, it's too confusing
fi

make perms >/dev/null 2>&1

while  [ "x$MINE_USER_EMAIL" = "x" ]
do
    PROMPT "Enter a contact e-mail address for web reports:"
    read MINE_USER_EMAIL
done

PROMPT "Enter a ORDINARY USER login name for your mine (default: $DEFAULT_USER)"
read MINE_USER
test "x$MINE_USER" = "x" && MINE_USER=$DEFAULT_USER

PROMPT "Enter a SUPER USER login name for your mine (default: $DEFAULT_SUPERUSER)"
read MINE_SUPERUSER
test "x$MINE_SUPERUSER" = "x" && MINE_SUPERUSER=$DEFAULT_SUPERUSER

MINE_USER_DB=database/$MINE_USER/sqlite3.db

if [ -f settings.py ]
then
    YESNO "The file 'settings.py' already exists - shall we replace it" && rm settings.py
fi

if [ -f $MINE_USER_DB ]
then
    YESNO "The database '$MINE_USER_DB' already exists - shall we replace it (THIS WILL DESTROY YOUR EXISTING MINE)" && rm $MINE_USER_DB
fi

# yes the args are visible during creation, no i can't be arsed yet to fix this
MINE_SECRET=`python -c 'import os, util.base64_mine as b64 ; print b64.encode(os.urandom(66))'`

if [ ! -f settings.py ]
then
    cat settings.py.tmpl |
    sed -e "s/%%MINE_SECRET%%/$MINE_SECRET/g" |
    sed -e "s/%%MINE_USER%%/$MINE_USER/g" |
    sed -e "s/%%MINE_USER_EMAIL%%/$MINE_USER_EMAIL/g" > settings.py
fi

if [ ! -d database/$MINE_USER ]
then
    mkdir database/$MINE_USER || exit 1
    chmod 755 database/$MINE_USER
fi

# go for it
echo ""
make dbsync  || exit 1

echo ""
while [ "x$MINE_USER_PASSWORD" = "x" ]
do
    echo "Enter a password for ORDINARY USER '$MINE_USER'"
    PROMPT "Password:"
    trap "stty echo ; exit" 1 2 3 15
    stty -echo
    read MINE_USER_PASSWORD
    stty echo
    echo ""
    trap "" 1 2 3 15

    PROMPT "Password (again):"
    trap "stty echo ; exit" 1 2 3 15
    stty -echo
    read MINE_USER_PASSWORD2
    stty echo
    echo ""
    trap "" 1 2 3 15

    if [ "x$MINE_USER_PASSWORD" != "x$MINE_USER_PASSWORD2" ]
    then
	echo "Error: Your passwords didn't match."
	MINE_USER_PASSWORD=""
    fi
done
DJANGO ./mineconfig.py create-user "$MINE_USER" "$MINE_USER_PASSWORD"

echo ""
echo "Enter a password for SUPER USER '$MINE_SUPERUSER'"
python manage.py createsuperuser --username $MINE_SUPERUSER --email $MINE_USER_EMAIL || exit 1

echo ""
echo setting up crypto seeds and keys...
DJANGO ./mineconfig.py init-crypto || exit 1

echo ""
echo done.
exit 0
