#-*- coding: utf-8 -*-
import os

import jinja2

from fabric.api import cd, env, lcd, local, prefix, put, run, settings, sudo, task
from fabric.contrib.project import rsync_project

from fabric.colors import *

from fabric.context_managers import shell_env

# change cwd to location of the fab file
local_path = os.path.dirname(os.path.abspath(env.real_fabfile)) + os.sep
os.chdir(local_path)
print(green('changing cwd to ' + local_path))


# from: https://github.com/scienceopen/hist-utils/blob/master/walktree.py

def walktree(root,pat):
    from os import walk, getcwd #not getcwdu, that's python 2 only
    from os.path import join,expanduser,isdir, isfile
    from fnmatch import filter
    root = expanduser(root)
    if isdir(root):
        found = []

        for top,dirs,files in walk(root):
            for f in filter(files,pat):
                found.append(join(top,f))

        if len(found)==0:
            found=None
    elif isfile(root):
        found = [root]
    else:
        exit("is " + root + " a file or directory?")

    return found

@task
def setup():
    setup_imagegenerator()
    setup_build()

def build_jinja2():
    # This should be farmed out to location-specific configuration…
    stuff = { 'gateway_name': 'SouperSalad',
              'captive_portal_url': 'http://surefi.com/',
              'ssid': 'Souper Salad Guest'}

    stuff = { 'gateway_name': 'Jose-Fi',
              'captive_portal_url': 'http://portal.pi-fi.co/',
              'ssid': 'Free Wi-Fi from Pi-Fi' }

    output_dir = 'build'
    directories_containing_templates = walktree('files', '*.jinja2')
    for directory in directories_containing_templates:
        base_directory = os.path.dirname(directory)
        filename = os.path.basename(directory)

        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(base_directory))
        jt = jenv.get_template(filename)

        output_filename = filename.replace('.jinja2', '')
        output_path = os.path.join(output_dir, base_directory, output_filename)

        fp = open(output_path, 'w')
        fp.write(jt.render(stuff).encode('utf8'))
        fp.close()

        print(base_directory, filename, jt, output_path)

@task
def setup_imagegenerator():
    print(red('Downloading latest image generator'))
    # Download latest image builder
    URL = 'http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/OpenWrt-ImageBuilder-ar71xx_generic-for-linux-x86_64.tar.bz2'
    local('wget -cq %s' % URL)
    local('aunpack -X . $(basename %s)' % URL)
    local('mv $(basename %s .tar.bz2) image-generator' % URL)

@task
def setup_build():
    print(red('Generating build folder'))
    local('cp -rl image-generator build')
    local('cp repositories.conf build')
    local('cp -r files build')
    build_jinja2()
    with lcd('build'):
        local('chmod 0600 files/etc/dropbear/authorized_keys')
        #local('chmod 0600 files/etc/shadow')
        local('chmod 0700 files/etc/dropbear/')

@task
def build():
    print(red('Building image (this is slow)'))
    with lcd('build'):
        local('mkdir -p dl')
        local('make image PROFILE=TEW712BR FILES="files" PACKAGES="dropbear nodogsplash rsync"')
        # TODO: Port this to fab commands, need to use native SSH
        print(green('Firmware image is now in build/bin/'))
        print('  Use build/bin/*/*factory.bin to flash a NEW, FACTORY SOFTWARE device')
        print('  Use build/bin/*/*sysupgrade.bin to flash a device that is running a previous OpenWrt image (i.e. anything you created w/ this tool)')
        print('')
        print(green('Some helper commands to copy a firmware image to a device (assuming the IP is the default, and you are behind the network for the device) and upgrade an exist running a pre-existing version of the software'))
        print('')
        print('scp build/bin/ar71xx/openwrt-ar71xx-generic-tew-712br-squashfs-sysupgrade.bin root@192.168.1.1:/tmp/')
        print('ssh root@192.168.1.1')
        print('sysupgrade -n /tmp/*sysupgrade.bin')

@task
def clean():
    local('rm -rf build image-generator')

@task
def distclean():
    clean()
    local('rm *.tar.bz2')
