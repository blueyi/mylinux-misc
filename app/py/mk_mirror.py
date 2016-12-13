#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 blueyi <blueyi@ubuntu>
#
# Distributed under terms of the MIT license.
import subprocess
import sys

def welcome_print(msg):
    print('*' * 70)
    print('     <<< ' + msg + ' >>>')
    print('*' * 70)



error_log_file = 'mk_mirror_error.log'
error_log = open(error_log_file, 'w')


def print_to_file(msg, file_opened=error_log):
    print(msg)
    file_opened.write(str(msg) + '\n')


def run_cmd(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    returncode = subprocess.call(tcall_cmd, shell=True)
    if returncode != 0 and ('grep' not in tcall_cmd):
        print_to_file('<<< ' + tcall_cmd + '>>> run failed! returncode:' + str(returncode))
        if not con :
            sys.exit(1)
    return returncode


def run_cmd_reout(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE)
    toutput = p.communicate()[0]
    if p.returncode != 0 and ('grep' not in tcall_cmd):
        print_to_file('<<< ' + tcall_cmd + '>>> run failed!')
        print_to_file(toutput)
        if not con :
            sys.exit(1)
    print(toutput)
    return toutput

url_file = 'url.txt'

wget_cmd = 'wget -r -p -np '
with open(url_file, 'r') as text:
    for tline in text:
        if len(tline.strip()) !=0 and 'http' in tline:
            tline = tline.strip()
            welcome_print('Downloading ' + tline)
            run_cmd(wget_cmd + tline, con = True)


error_log.close()

is_del_err_file = True
with open(error_log_file, 'r') as err:
    for line in err:
        if len(line.strip()) != 0:
            is_del_err_file = False

if is_del_err_file:
    run_cmd('rm -f ' + error_log_file)

welcome_print('Download site Success!')
