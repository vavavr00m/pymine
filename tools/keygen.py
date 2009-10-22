#!/usr/bin/python

"""docstring goes here""" # :-)

import os
import sys
import getopt
import base64

def usage():
    print "wtf?" # let nobody ever say i don't write documentation

def main(argv):
    nbytes = 66

    try:
	opts, args = getopt.getopt(argv, "hn:", ["help", "nbytes="])

    except getopt.GetoptError:
	usage()
	sys.exit(1)

    for opt, arg in opts:
	if opt in ('-h', '--help'):
	    usage()
	    sys.exit()
	elif opt in ('-n', '--nbytes'):
	    nbytes = int(arg)

    bytes = os.urandom(nbytes)

    print base64.b64encode(bytes, '!@')

if __name__ == "__main__":
    main(sys.argv[1:])
