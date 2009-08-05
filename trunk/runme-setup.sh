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

MINEUSER=$USER

if [ -f settings.py ]
then
    echo "The file 'settings.py' already exists"
    if YESNO "Shall we nuke it and replace it"
    then
	rm settings.py
    fi
fi


DB=database/$MINEUSER/sqlite3.db

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
    read EMAIL 

    YESNO "You entered $EMAIL ; is this OK" && break
done

test -f settings.py || cp settings.py,master settings.py
test -d database/$MINEUSER || mkdir database/$MINEUSER || exit 1

make clean
make perms
make dbsync

echo "We shall use '$MINEUSER' as your mine database superuser login name."
echo "You will now be asked to select a password for '$MINEUSER'"
python manage.py createsuperuser --username $MINEUSER --email $EMAIL

