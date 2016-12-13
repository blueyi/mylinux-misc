
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

error_log_file = 'misc_err.log'
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
# clone url to dir from misc.cmd
def git_clone(turl, tdir):
    dot_git_path = tdir + '/.git'
    if not os.path.exists(dot_git_path):
        git_cmd = 'git clone ' + turl + ' ' + tdir
        print(git_cmd)
        run_cmd(git_cmd, con = True)


welcome_print('Some system config: git, vim, hexo etc.')
misc_cmd_file = curr_path + '/' + 'misc.cmd'
with open(misc_cmd_file, 'r') as text:
    for tline in text:
        if tline[0] != '#' and len(tline.strip()) != 0:
            if '~/' in tline:
                tline = tline.replace('~', user_path)
            tcmd = tline.strip().split('#')[0]
            print(tcmd)
            tgit_url = tcmd.split()
            if '.git' in tgit_url[0]:
                git_clone(tgit_url[0], tgit_url[1])
            else:
                print(tcmd)
                run_cmd(tcmd, con = True)


error_log.close()

is_del_err_file = True
with open(error_log_file, 'r') as err:
    for line in err:
        if len(line.strip()) != 0:
            is_del_err_file = False

if is_del_err_file:
    run_cmd('rm -f ' + error_log_file)


welcome_print('misc.cmd config success!')
