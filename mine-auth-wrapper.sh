#!/bin/sh

MINEURL=http://127.0.0.1:9862
MINEDIR=`dirname $0`
MINEDIR=`( cd $MINEDIR ; pwd )`
MINECOOKIEJAR="${MINEDIR}/etc/cookies.txt"

CURLFLAGS=""

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

DEFAULT_USER=pickaxe

case $1 in
    login)
	if [ "x$2" = "x" ]
	then 
	    PROMPT "Enter a login name for your mine (default: $DEFAULT_USER)"
	    read MINE_USER
	    test "x$MINE_USER" = "x" && MINE_USER=$DEFAULT_USER
	else
	    MINE_USER="$2"
	fi

	if [ "x$3" = "x" ]
	then
	    PROMPT "$MINE_USER password:"
	    trap "stty echo ; exit" 1 2 3 15
	    stty -echo
	    read MINE_USER_PASSWORD
	    stty echo
	    echo ""
	    trap "" 1 2 3 15
	else
	    MINE_USER_PASSWORD="$3"
	fi

	curl --request POST $CURLFLAGS --fail -c $MINECOOKIEJAR ${MINEURL}/login.html -F "username=${MINE_USER}" -F "password=${MINE_USER_PASSWORD}"
	echo "curl exit status: $?"
	;;

    logout)

	curl --request GET $CURLFLAGS --fail -b $MINECOOKIEJAR ${MINEURL}/logout.html
	echo "curl exit status: $?"
	;;

    *)
	echo "usage:"
	echo "    $0 login [username [password]]"
	echo "    $0 logout"
	;;
esac

exit 0
