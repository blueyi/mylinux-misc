#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 blueyi <blueyi@blueyi-ubuntu>
#
# Distributed under terms of the MIT license.

import subprocess
import sys
import os
import time

"""
Some function and const value
"""

# print some important string
def welcome_print(msg):
    print('*' * 70)
    print('   <<< ' + msg + ' >>>')
    print('*' * 70)

# def print_to_file(msg, file_opened=error_log):
#     print(msg)
#     file_opened.write(str(msg) + '\n')

# run an shell command in subprocess
def run_cmd_reout(tcall_cmd, goOnRun = False, isOutPut = True, jumpErr = False, isReturnCode = False):
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
    toutput = p.communicate()[0]
    if p.returncode != 0 and not jumpErr:
        print('<<< ' + tcall_cmd + ' >>> run failed! returncode:' + str(p.returncode))
#        print_to_file('<<< ' + tcall_cmd + ' >>> run failed! returncode:' + str(returncode), file_opened)
        if not goOnRun :
            sys.exit(1)
    if isOutPut :
        print(toutput)
    if isReturnCode :
        return p.returncode
    else :
        return toutput

# add command to supervirsord

def addToSupervisord(cmdName, cmd) :
    ubuntu_su_conf_path = '/etc/supervisor/conf.d/'
    log_dir = '/var/log/supervisor/'
    if not os.path.exists(ubuntu_su_conf_path):
        run_cmd_reout('mkdir -p ' + ubuntu_su_conf_path)

    if not os.path.exists(log_dir):
        run_cmd_reout('mkdir -p ' + log_dir)

    configFileOpened = open(ubuntu_su_conf_path + cmdName + '.conf', 'w')
    config_content = ''
    if '/' in cmd[:cmd.find(' ')] :
        config_content = '[program:' + cmdName + ']' + '\n' + \
                'command = ' + cmd + '\n' + \
                'directory = ' + cmd[:cmd.rfind('/')+1] + '\n' + \
                'user = root' + '\n' + \
                'autostart = true' + '\n' + \
                'autorestart = true' + '\n' + \
                'stdout_logfile = ' + log_dir + cmdName + '.log' + '\n' + \
                'stderr_logfile = ' + log_dir + cmdName + '_err.log' + '\n'
    else :
        config_content = '[program:' + cmdName + ']' + '\n' + \
                'command = ' + cmd + '\n' + \
                'user = root' + '\n' + \
                'autostart = true' + '\n' + \
                'autorestart = true' + '\n' + \
                'stdout_logfile = ' + log_dir + cmdName + '.log' + '\n' + \
                'stderr_logfile = ' + log_dir + cmdName + '_err.log' + '\n'

    configFileOpened.write(config_content)
    configFileOpened.close()
    run_cmd_reout('systemctl enable supervisor')
    run_cmd_reout('systemctl start supervisor')
    run_cmd_reout('supervisorctl reload')





