#!/usr/bin/python3
from fabric.api import env, put, run, local
from time import strftime
from datetime import datetime
from os import path

env.hosts = ['54.210.107.117', '18.204.10.96']
env.user = 'ubuntu'
env.sudo_user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes
    an archive to your web server"""

    if not path.exists(archive_path):
        return False
    try:
        tgzfile = archive_path.split("/")[-1]
        print(tgzfile)
        filename = tgzfile.split(".")[0]
        print(filename)
        put(archive_path, '/tmp/')
        run("sudo mkdir -p /data/web_static/releases/{}/".format(filename))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgzfile, filename))
        run("sudo rm /tmp/{}".format(tgzfile))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(filename, filename))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(filename))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        return True
    except Exception as e:
        return False


def deploy():
    """run the 2 functions"""

    path = do_pack()
    if not path:
        return False

    return do_deploy(path)
