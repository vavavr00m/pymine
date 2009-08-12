#!/bin/sh

MINE_USER=$USER
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

make clean
make perms

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
MINE_SECRET=`./keygen.py`

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
make dbsync

# last step
echo "We shall use '$MINE_USER' as your mine database superuser login name."
echo "You will now be asked to select a password for '$MINE_USER'"
python manage.py createsuperuser --username $MINE_USER --email $MINE_EMAIL

exit 0 
