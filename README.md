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

Place files to include in an image into the "files" directory.

Files can be Jinja2 templates, with template variables loaded from configuration files.

At the moment, configuration files are not yet implemented, but "fabfile.py", in the `build_jinja2()` function, can be modified appropriately.
Configuration settings that can be changed include node name (a unique identifier for the device in question), wireless SSID, and captive portal page.

Run `fab --list` to get a list of all tasks that can be run. To build an image, run:

    fab setup # Runs both setup_imagegenerator




## Legal

Copyright (c) 2014–2015 Pi-Fi, LLC. All Rights Reserved.

Software licensed under GNU GPLv3 (see LICENSE).
