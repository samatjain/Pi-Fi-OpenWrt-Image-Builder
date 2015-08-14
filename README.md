# OpenWrt Image Generator for Pi-Fi

Easily creates OpenWrt images, using OpenWrt's Image Generator (AKA Builder) tool, with custom software, files, and settings included.

## Dependencies

Install:

 * [fabric](http://www.fabfile.org/)
 * [jinja2](http://jinja.pocoo.org/)

Because fabric needs Python 2, please use Python 2.
fabric does not import libraries contained within virtualenvs so it's best you install these libraries system-wide.

On Debian/Ubuntu, these are installed with:

    sudo aptitude install fabric python-jinja2

## Use

Place files to include in an image into the "files" directory. Password authentication is disabled, so please add your SSH keys for remote access (required for upgrading or any kind of maintenance!) to files/etc/dropbear/authorized_keys.

Files can be Jinja2 templates, with template variables loaded from configuration files.

At the moment, configuration files are not yet implemented, but "fabfile.py", in the `build_jinja2()` function, can be modified appropriately.
Configuration settings that can be changed include node name (a unique identifier for the device in question), wireless SSID, and captive portal page.

Run `fab --list` to get a list of all tasks that can be run. To build an image, run:

    fab setup # Runs both setup_imagegenerator setup_build automatically
    fab build

After running `fab build`, firmware files will be within 'build/bin', depending on architecture.

Files named `*factory.bin` can be used to upgrade a stock, from-the-factory device through their Web interface.

Files named `*sysupgrade.bin` can be used to upgrade a device already running OpenWrt, i.e. one that has had images from this tool flashed to it.

Images from this tool do not include a Web interface, so you must use SSH and the command-line sysupgrade tool to upgrade firmware images. Commands that do this will look like:

    scp build/bin/ar71xx/openwrt-ar71xx-generic-tew-712br-squashfs-sysupgrade.bin root@192.168.1.1:/tmp/
    ssh root@192.168.1.1
    sysupgrade -n /tmp/*sysupgrade.bin

## Known issues

 * No configuration files for creating firmware images, you must directly edit fabfile.py
 * Tool assumes building for the TRENDnet TEW-712BR and the ar71xx CPU architecture. At some point other devices, and other architectures, will be supported.

## Legal

Copyright (c) 2014–2015 Pi-Fi, LLC. All Rights Reserved.

Software licensed under GNU GPLv3 (see LICENSE).
