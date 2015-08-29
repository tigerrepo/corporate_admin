import os
import string
import random
import datetime


def generate_random_password(length=16, charset=string.ascii_letters + string.digits):
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(charset) for i in range(length))


def format_date(date, orig_format, res_format):
    return datetime.datetime.strptime(date, orig_format).strftime(res_format)
