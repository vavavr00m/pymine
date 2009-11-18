#!/bin/sh

MINEURL=http://127.0.0.1:9862

MINEDIR=`dirname $0`
MINEDIR=`( cd $MINEDIR ; pwd )`

MINECOOKIEJAR="${MINEDIR}/etc/cookies.txt"

CURLFLAGS=""

case $1 in
    login)
	if [ "x$2" = "x" ]
	then 
	    echo "enter username for mine at $MINEURL (def: pickaxe)"
	    read MINEUSER
	    test "x$MINEUSER" = x && MINEUSER="pickaxe"
	    echo "confirmed: your username is '$MINEUSER'"
	else
	    MINEUSER="$2"
	fi

	if [ "x$3" = "x" ]
	then
	    echo enter password for mine user $MINEUSER
	    read MINEPASS
	else
	    MINEPASS="$3"
	fi

	curl --request POST $CURLFLAGS --fail -c $MINECOOKIEJAR ${MINEURL}/login.html -F "username=${MINEUSER}" -F "password=${MINEPASS}"
	echo "login status: $?"

	;;

    logout)

	curl --request GET $CURLFLAGS --fail -b $MINECOOKIEJAR ${MINEURL}/logout.html
	echo "logout status: $?"

	;;

    *)
	echo "usage:"
	echo "    $0 login [username [password]]"
	echo "    $0 logout"
	;;
esac

exit 0
