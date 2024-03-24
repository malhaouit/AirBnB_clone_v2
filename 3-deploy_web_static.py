#!/usr/bin/python3
"""
A Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to the web servers.
Current file: 3-deploy_web_static.py
"""
from fabric.api import env, run, put, local
import os
from datetime import datetime

env.hosts = ['54.174.153.120', '18.204.14.78']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """
    Generates a .tgz archive from contents of web_static
    """
    try:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)
        # Ensure versions directory exists
        local("mkdir -p versions")
        # Create archive with compression
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploys the archive to the servers"""

    # Check if the archive exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Transfer the archive
        put(archive_path, "/tmp/")
        # Extract the file name and remove the extension
        file_name = archive_path.split("/")[-1]
        name_no_ext = file_name.split('.')[0]
        # Path
        path = "/data/web_static/releases/"
        # Create directory for the archive on the server
        run('mkdir -p {}{}'.format(path, name_no_ext))
        # Uncompress the archive to the folder on the server
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, name_no_ext))
        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))
        # Move the content to the correct folder
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, name_no_ext))
        # Remove the source folder
        run('rm -rf {}{}/web_static'.format(path, name_no_ext))
        # Delete the current symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, name_no_ext))
        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and deploys an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
