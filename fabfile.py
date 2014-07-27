from fabric.api import *
from fabric.operations import put
import os
import getpass

env.hosts = [
    #'issackelly@10.0.0.28',
    'issackelly@192.168.1.100',
]

env.use_ssh_config = True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@task
def update():
    local('rsync -azv %s/ %s:/home/issackelly/Projects/art/snowwhite --exclude="*.pyc" --exclude=".git" --exclude="env"' % (BASE_DIR, env.hosts[0]))
    sudo('cp /home/issackelly/Projects/art/snowwhite/config/supervisord.conf /etc/supervisor/supervisord.conf')
    sudo("reboot")

@task
def light_update():
    local('rsync -azv %s/ %s:/home/issackelly/Projects/art/snowwhite --exclude="*.pyc" --exclude=".git" --exclude="env"' % (BASE_DIR, env.hosts[0]))
    sudo('supervisorctl restart runner')
    sudo('supervisorctl restart controller')
