import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
import time
import datetime

logger = logging.getLogger("SipTables")

def tables_all(request):
    if request.method == 'POST':
        print 'Hello'
