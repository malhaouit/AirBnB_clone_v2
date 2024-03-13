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


def do_deploy(archive_path):
    """Deploy the archive to the servers"""
    # Check if the archive exists
    if not os.path.isfile(archive_path):
        return False

    try:
        # Transfer the archive
        put(archive_path, "/tmp/")
        # Extract the file name
        file_name = os.path.basename(archive_path)
        # Remove the extension from the file name
        name_no_ext = file_name.split('.')[0]
        # Create directory for the archive on the server
        run('mkdir -p /data/web_static/releases/{}'.format(name_no_ext))
        # Uncompress the archive to the folder on the server
        run('tar -xzf /tmp/{} -C '
            '/data/web_static/releases/{}/'.format(file_name, name_no_ext))
        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))
        # Move the content to the correct folder
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(name_no_ext, name_no_ext))
        # Remove the source folder
        run('rm -rf '
            '/data/web_static/releases/{}/web_static'.format(name_no_ext))
        # Delete the current symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} '
            '/data/web_static/current'.format(name_no_ext))

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print("An error occurred: {}".format(e))
        return False


def deploy():
    """
    Creates and deploys an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
