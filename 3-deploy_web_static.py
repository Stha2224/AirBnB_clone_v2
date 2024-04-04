#!/usr/bin/python3
""" Fabric script to call do_deploy() and do_pack() methods
"""
import os
import time
from fabric.api import *
from pathlib import Path

env.user = 'ubuntu'
env.hosts = ['35.243.219.137', '35.237.245.133']


def do_pack():
    """ Archives web_static contents as a tarball to /versions folder
    """
    date_var = time.strftime("%Y%m%d%H%M%S")
    directory = "versions/web_static_{}.tgz".format(date_var)

    try:
        local("mkdir -p ./versions && tar -zcvf ./{} ./web_static"
              .format(directory))
    except:
        return None
    else:
        return directory


def do_deploy(archive_path):
    """ Uploads archive to /tmp/, uncompresses, cleans up
    """
    p = Path(archive_path)
    f_full = p.name
    f_noext = p.stem

    if not os.path.exists(archive_path):
        return False
    else:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(f_noext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(f_full, f_noext))
        run("rm /tmp/{}".format(f_full))
        run("mv /data/web_static/releases/{}/web_static/*\
    /data/web_static/releases/{}/".format(f_noext, f_noext))
        run("rm -rf /data/web_static/releases/{}/web_static".format(f_noext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(f_noext))
        return True


def deploy():
    """ Calls do_pack() and do_deploy() methods
    """

    pack_dir = do_pack()
    if pack_dir is None:
        return False

    return do_deploy(pack_dir)
