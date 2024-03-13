#!/usr/bin/python3
"""
A Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives.
Current file: 100-clean_web_static.py
"""
from fabric.api import *
import os

env.hosts = ['54.174.153.120', '18.204.14.78']
env.user = "ubuntu"
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """Deletes out-of-date archives."""
    number = int(number)
    if number in [0, 1]:
        number = 1
    else:
        number += 1

    # Local cleanup
    local('ls -tr versions/web_static_* | head -n -{} | xargs rm -f'.format(number))

    # Remote cleanup
    with cd('/data/web_static/releases'):
        run('ls -tr web_static_* | head -n -{} | xargs rm -rf'.format(number))
