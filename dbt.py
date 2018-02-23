#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""

import argparse
import sys

try:
    COMMAND = sys.argv[1].lower().replace("-", "_")
except IndexError as e:
    print("dbt requires a COMMAND")
    sys.exit(1)

ARGS = sys.argv[2:]

parser = argparse.ArgumentParser(description='docker-build-tool')

class DockerBuildTool(object):

    def __init__(self):
        self._downloader = None

    def download(self, src, dst):
        if sys.version_info[0] == 2:
            from urllib import urlretrieve
        else:
            from urllib.request import urlretrieve

        urlretrieve(src, dst)

    def command_extract(self):
        parser.add_argument('-c', '--clean', dest="clean", action="store_true")

    def command_prepare_shell(self):
        self.download("https://raw.githubusercontent.com/klamar/docker-build-tool/master/res/bash/bashrc", "/root/.bashrc")

    def command_dl(self):
        parser.add_argument('src', metavar='SRC', type=str)
        parser.add_argument('dst', metavar='DST', type=str)
        args = parser.parse_args(ARGS)

        self.download(args.src, args.dst)


if __name__ == '__main__':
    dbt = DockerBuildTool()
    getattr(dbt, "command_" + COMMAND)()
