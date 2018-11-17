
# if __name__ == "__main__":

bind = 'unix:/var/run/swim.sock'
# bind = '127.0.0.1:50009'

#workers = 2

#worker_connections = 1000
#max_requests = 1000

debug = True
#deamon = True
#pidfile = '/var/run/swim.pid'

#user = 'nginx'
#group = 'nginx'

errorlog = '/var/log/gunicorn/swim-error.log'
accesslog = '/var/log/gunicorn/swim-access.log'

loglevel = 'info'
proc_name = 'swim'
