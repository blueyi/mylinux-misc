#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 blueyi <blueyi@ubuntu>
#
# Distributed under terms of the MIT license.

from common import *

"""
install shadowsocks python server
run by root
"""


if os.geteuid() != 0:
    print('Please run the script by "root"!')
    sys.exit(1)

# install pip
pip_install_cmd = 'apt-get install python-pip'
run_cmd_reout(pip_install_cmd, goOnRun=True)

# install shadowsocks
install_ssserver_cmd = 'pip install shadowsocks'
run_cmd_reout(install_ssserver_cmd, goOnRun=True)

# add to supervisord
cmd = 'ssserver -p 10320 -k blueyiniu -m aes-128-cfb'
addToSupervisord('ssserver', cmd)





