# http://www.djangosnippets.org/snippets/290/

from django.db import connection
from django.conf import settings
import os

class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """
    def process_response(self, request, response):
        if len(connection.queries) > 0 and settings.DEBUG:
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',',', ')
                print ">%s %s" % (query['time'], nice_sql)
        return response
