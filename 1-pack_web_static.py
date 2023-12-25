#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """ A script that generates an archive contents of the web_static foler"""

    filename = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None
