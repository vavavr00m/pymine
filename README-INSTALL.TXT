prerequisites for pymine:

	python 2.5.1 or later
	django 1.0.2 or later

upcoming:

    lxml (and dependencies: libxml2, libxslt)
    http://codespeak.net/lxml/installation.html#macos-x
    http://lsimons.wordpress.com/2008/08/31/how-to-install-lxml-python-module-on-mac-os-105-leopard/

how to install:

    ./runme-setup.sh

how to install with less typing:

    env MINE_EMAIL=alec.muffett@gmail.com ./runme-setup.sh

questions:

should we let subscribers see their own comments upon existing items?
it will have to be possible somehow to permit blog-style
functionality, but if we do it all with authenticated minekey access,
is there not the possibility of someone submitting a comment and when
retreiving it from the mine having it rewritten to provide access to
the user's other objects?  

that is a risk, therefore we must consider whether url-rewriting
should only apply to user's items
