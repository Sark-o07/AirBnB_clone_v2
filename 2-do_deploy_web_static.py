#!/usr/bin/python3
"""
Fabric script method:
    do_deploy: deploys archive to webservers
Usage:
    fab -f 2-do_deploy_web_static.py
    do_deploy:archive_path=versions/web_static_20170315003959.tgz
    -i my_ssh_private_key -u ubuntu
"""
from fabric.api import env, put, sudo
import os.path
env.hosts = ['54.210.107.117', '18.204.10.96']
env.user = 'ubuntu'
env.key_filename = os.path.expanduser('~/.ssh/id_rsa')


def do_deploy(archive_path):
    """
    Distribute an archive to your web servers.
    Args:
        archive_path: the path to the archive to deploy.
    Returns:
        True if all operations have been done correctly,
        otherwise returns False.
    """
    # Check if the archive exists
    if not os.path.isfile(archive_path):
        return False

    # Get the archive filename (without extension)
    tgzfile = archive_path.split("/")[-1]
    print(tgzfile)
    filename = tgzfile.split(".")[0]
    print(filename)

    try:
        # Upload the archive the archive to the /tmp/ dir of the web server
        put(archive_path, '/tmp/')

        # Create the releases directory if it doesn't exist
        sudo('mkdir -p /data/web_static/releases/{}/'.format(filename))

        # Uncompress the archive to the releases directory
        sudo('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
             .format(filename, filename))

        # Delete the archive from the web server
        sudo('rm /tmp/{}.tgz'.format(filename))

        # Move the contents of the release directory up one level
        sudo('mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/'.format(filename, filename))

        # Delete the now-empty web_static directory
        sudo('rmdir /data/web_static/releases/{}/web_static'.format(filename))

        # Create a new symbolic link /data/web_static/current
        sudo('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        sudo('ln -s /data/web_static/releases/{}/ /data/web_static/current'
             .format(filename))

        # Deployment successful
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
