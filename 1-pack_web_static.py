#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo.
Current file: 1-pack_web_static.py
"""
from fabric.api import local, run
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from contents of web_static
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)

    try:
        # Ensure versions directory exists
        local("mkdir -p versions")
        # Create archive with compression
        local("tar -cvzf {} web_static".format(archive_path))
        print("Archive created: {}".format(archive_path))
        return archive_path
    except Exception as e:
        print("An error occurred: {}".format(e))
        return None
