# FAQs #

## Error: No module named pymine.api ##

### Issue ###

I'm trying to setup pymine on our server. I've checkouted svn code and installed missing packages. After running make setup in code root I've got the following:

```
Entering directory '/svn/pymine-read-only'
python manage.py syncdb --noinput --traceback
Error: No module named pymine.api
make[1]: *** [dbsync] Error 1
make[1]: Leaving directory '/svn/pymine-read-only'
make: *** [setup] Error 1
```

what have I done wrong ?

### Answer ###

That `pymine-read-only` is the problem; regardless of the documented GoogleCode checkout process, the pymine directory needs to be called "pymine", otherwise the package import mechanism gets confused.

  1. Rename that directory to "pymine".
  1. And then do `make clobber`
  1. And then `make setup`