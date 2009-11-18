#!/bin/sh

echo ""
echo setting up pymine in `pwd` via $0 $@
echo ""

MINE_USER=$USER
MINE_SUPERUSER=pickaxe
MINE_DB=database/$MINE_USER/sqlite3.db

YESNO() {
    while :
    do
	echo "$@ ? (y/n) \c"
	read answer

	case "$answer" in
	    [Yy]*) return 0 ;;
	    [Nn]*) return 1 ;;
	    *) echo "please answer yes or no."
	esac
    done
}

(
make perms || exit 1
make clean || exit 1
) >/dev/null 2>&1

if [ -f settings.py ]
then
    echo "The file 'settings.py' already exists"
    if YESNO "Shall we nuke it and replace it"
    then
	rm settings.py
    fi
fi

if [ -f $MINE_DB ]
then
    echo "The mine database '$MINE_DB' already exists"
    if YESNO "Shall we nuke it and replace it (THIS WILL IRREVOCABLY DESTROY YOUR MINE)"
    then
	rm $MINE_DB
    fi
fi

if  [ "x$MINE_EMAIL" = "x" ]
then
    while :
    do
	echo "Enter your e-mail address: \c"
	read MINE_EMAIL
	YESNO "You entered $MINE_EMAIL ; is this OK" && break
    done
fi

# yes the args are visible during creation, no i can't be arsed yet to fix this
MINE_SECRET=`./tools/keygen.py`

if [ ! -f settings.py ]
then
    cat settings.py.tmpl |
    sed -e "s/%%MINE_SECRET%%/$MINE_SECRET/g" |
    sed -e "s/%%MINE_USER%%/$MINE_USER/g" |
    sed -e "s/%%MINE_EMAIL%%/$MINE_EMAIL/g" > settings.py
fi

if [ ! -d database/$MINE_USER ]
then
    mkdir database/$MINE_USER || exit 1
    chmod 755 database/$MINE_USER
fi

# go for it
make dbsync  || exit 1

# last step

echo ""
echo "Authentication:"
echo ""
echo "We shall use '$MINE_SUPERUSER' as your mine database superuser login name."
echo "You will now be asked to select a password for '$MINE_SUPERUSER'"

python manage.py createsuperuser --username $MINE_SUPERUSER --email $MINE_EMAIL || exit 1

cat <<EOF

Thank you.

------------------------------------------------------------------

No method exists in Django for creating non-superusers, so we strongly
recommend you log into your mine as the superuser and create a basic,
non-privileged user (eg: "$MINE_USER") for your day-to-day usage, and
then log out, and do not again log into the mine as superuser unless
really required.

At some point we will work around this.

You may now "make server" to launch your development mine, after which
you may do "make client" in another window to open a browser on it.

Remember to initially use the login name "$MINE_SUPERUSER" and the
password you provided.

------------------------------------------------------------------

EOF

exit 0
