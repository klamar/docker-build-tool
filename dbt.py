#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""

import argparse
import json
import sys

import os

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

    def command_apt_install(self):
        pass

    def command_tpl(self):
        parser.add_argument('template', metavar='TEMPLATE', type=str)
        parser.add_argument('output', metavar='OUTPUT', type=str)
        parser.add_argument('-e', '--env', dest='env_file', type=str, help='path to environment file')
        parser.add_argument('-j', '--json', dest='json_file', type=str, help='path to json file')

        args = parser.parse_args(ARGS)

        context = os.environ

        if args.env_file:
            with open(args.env_file) as f:
                env_contents = f.read()
            env_extra = [l.strip() for l in env_contents.splitlines() if l.strip()]
            for line in env_extra:
                key, value = line.split("=")
                context[key] = value.strip(' "\'')

        if args.json_file:
            with open(args.json_file) as f:
                json_data = json.loads(f.read())
            context.update(json_data)

        with open(args.template) as f:
            template_contents = f.read()

        rendered = template_contents % context

        with open(args.output, "w") as f:
            f.write(rendered)


    def command_replace(self):
        parser.add_argument('search', metavar='SEARCH', type=str)
        parser.add_argument('replace', metavar='REPLACE', type=str)
        parser.add_argument('path', metavar='PATH', type=str)
        args = parser.parse_args(ARGS)

        with open(args.path) as f:
            contents = f.read()

        if not args.search in contents:
            print("Unable to find '%s' in %s" % (args.search, args.path))
            exit(1)

        contents = contents.replace(args.search, args.replace)

        with open(args.path, 'w') as f:
            f.write(contents)

    def command_install_composer(self):
        r = os.system('curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer')
        assert r == 0

if __name__ == '__main__':
    dbt = DockerBuildTool()
    getattr(dbt, "command_" + COMMAND)()
