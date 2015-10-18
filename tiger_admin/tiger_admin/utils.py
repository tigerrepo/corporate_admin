import os
import string
import random
import datetime
from django.conf import settings

def generate_random_password(length=16, charset=string.ascii_letters + string.digits):
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(charset) for i in range(length))


def format_date(date, orig_format, res_format):
    return datetime.datetime.strptime(date, orig_format).strftime(res_format)

def upload_image(f, directory):
    print f
    ext = str(f).split(".")[-1]
    filename = "%s.%s" % (generate_random_password(length=8), ext)
    filepath = '%s/%s' % (directory, filename)
    print filepath
    print directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename
