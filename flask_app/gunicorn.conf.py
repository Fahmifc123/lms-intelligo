from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

chdir = '/home/intelli3/lms.intelligo.id/flask_app'
bind = '127.0.0.1:52418'
max_requests = 100
workers = 1
worker_class = 'tornado'
errorlog = 'error.log'
loglevel = 'error'
wsgi_app = 'wsgi:app'
pidfile = 'gunicorn.pid'
pythonpath = '/home/intelli3/.asdf/shims/python'
daemon = True
