#! /usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import subprocess
import os
import sys


def welcome_print(msg):
    print('*' * 70)
    print('     <<< ' + msg + ' >>>')
    print('*' * 70)


# Modify process environment
def shell_source(script):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

error_log_file = 'link_err.log'
error_log = open(error_log_file, 'w')


def print_to_file(msg, file_opened=error_log):
    print(msg)
    file_opened.write(str(msg) + '\n')


def run_cmd(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    returncode = subprocess.call(tcall_cmd, shell=True, executable = '/bin/bash')
    if returncode != 0 and ('grep' not in tcall_cmd):
        print_to_file('<<< ' + tcall_cmd + '>>> run failed!')
        if not con :
            sys.exit(1)
    return returncode


def run_cmd_reout(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable = '/bin/bash')
    toutput = p.communicate()[0]
    if p.returncode != 0 and ('grep' not in tcall_cmd):
        print_to_file('<<< ' + tcall_cmd + '>>> run failed!')
        print_to_file(toutput)
        if not con :
            sys.exit(1)
    print(toutput)
    return toutput


# path
# script path
curr_path = os.path.split(os.path.realpath(__file__))[0]
# user path
user_path = os.path.expanduser('~')

# ---Create soft link for config file---
welcome_print('Linking user config file')
config_link_file = curr_path + '/' + 'config_link.json'


def link_cmd(sor, dest):
    cmd = 'ln -s -f '
    cmd = cmd + sor + ' ' + dest
    return cmd


# Link some config to mylinux-misc directory
def config_link(file_path):
    link_dict = {}
    with open(file_path, 'r') as text:
        for tline in text:
            if tline[0] != '#' and len(tline.strip()) != 0 and ('home' in tline or '~/' in tline):
                tline = tline.replace('~', user_path)
                tlink = tline.strip().split('#')[0].split()
                if len(tlink) > 1:
                    link_dict[tlink[0]] = tlink[1]
    for key, value in link_dict.items():
        if os.path.isfile(value):
            run_cmd('mv ' + value + ' ' + value + '.bak')
        print(value + ' -> ' + key)
        run_cmd(link_cmd(curr_path + '/' + key, value))

config_link(config_link_file)


error_log.close()

is_del_err_file = True
with open(error_log_file, 'r') as err:
    for line in err:
        if len(line.strip()) != 0:
            is_del_err_file = False

if is_del_err_file:
    run_cmd('rm -f ' + error_log_file)


welcome_print('Link user config file Success!')
