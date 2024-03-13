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
    number = int(number) + 1
    # Local cleaning
    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number))

    # Remote cleaning
    with cd("/data/web_static/releases"):
        run("ls -t | grep web_static | "
            "tail -n +{} | xargs rm -rf".format(number))
