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
    """Cleanup"""
    number = int(number)
    keep_count = number if number >= 1 else 1

    # Define commands for local and remote cleanup
    local_cleanup_cmd = 'ls -t versions/web_static_* | tail -n +{} | xargs rm -rf'.format(keep_count + 1)
    remote_cleanup_cmd = 'ls -t web_static_* | tail -n +{} | xargs rm -rf'.format(keep_count + 1)

    # Perform local cleanup
    local(local_cleanup_cmd)

    # Perform remote cleanup on all hosts
    with cd('/data/web_static/releases'):
        run(remote_cleanup_cmd)
