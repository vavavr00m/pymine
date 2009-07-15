IP_ADDRESS=127.0.0.1
IP_PORT=9862
IP_TUPLE=$(IP_ADDRESS):$(IP_PORT)

client:
	open http://$(IP_TUPLE)/

server:
	python manage.py runserver $(IP_TUPLE)

clean:
	-rm *~ */*~
	-rm *.pyc */*.pyc

sync:
	python manage.py validate 
	python manage.py sqlall web
	python manage.py syncdb

shell:
	python manage.py shell

