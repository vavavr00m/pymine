#!/bin/sh

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

MINE_USER=$USER

if [ -f settings.py ]
then
    echo "The file 'settings.py' already exists"
    if YESNO "Shall we nuke it and replace it"
    then
	rm settings.py
    fi
fi


DB=database/$MINE_USER/sqlite3.db

if [ -f $DB ]
then
    echo "The mine database '$DB' already exists"
    if YESNO "Shall we nuke it and replace it (THIS WILL IRREVOCABLY DESTROY YOUR MINE)"
    then
        rm $DB
    fi
fi

while :
do
    echo "Enter your e-mail address: \c"
    read MINE_EMAIL 

    YESNO "You entered $MINE_EMAIL ; is this OK" && break
done

if [ ! -f settings.py ]
then
    cat settings.py,master |
    sed -e "s/%%MINE_USER%%/$MINE_USER/g" |
    sed -e "s/%%MINE_EMAIL%%/$MINE_EMAIL/g" > settings.py 
fi

test -d database/$MINE_USER || mkdir database/$MINE_USER || exit 1

make clean
make perms
make dbsync

echo "We shall use '$MINE_USER' as your mine database superuser login name."
echo "You will now be asked to select a password for '$MINE_USER'"
python manage.py createsuperuser --username $MINE_USER --email $MINE_EMAIL

