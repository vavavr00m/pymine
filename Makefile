test:
	for i in *.py ; do echo testing $$i ... ; python $$i || break ; done
clean:
	reaper3
	rm *.pyc
