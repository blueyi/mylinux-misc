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

welcome_print('Installing software and config your system dependent')


def del_self():
#    run_cmd('rm -f ' + sys.argv[0])
    pass


# Modify process environment
def shell_source(script):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

apt_list = ['ubuntu', 'debian']
rpm_list = ['fedora', 'centos']
sys_distribution = platform.linux_distribution()[0].lower()
# print(sys_distribution)


def is_list_in_str(tlist, tstr):
    for item in tlist:
        if item in tstr:
            return True
    return False


error_log_file = 'install_err.log'
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



# Install software
root_cmd = 'sudo python ' + 'su_cmd.py'
run_cmd(root_cmd, con = True)


# path
# script path
curr_path = os.path.split(os.path.realpath(__file__))[0]
# user path
user_path = os.path.expanduser('~')

# ---Create soft link for config file---
link_cmd = 'python ' + 'link.py'
run_cmd(link_cmd, con = True)


# ---Some user config from command file---
misc_cmd = 'python ' + 'misc.py'
run_cmd(misc_cmd, con = True)

# ---Other configure---
# ---Install hexo---
# bashrc_path = user_path + '/' + '.bashrc'
# shell_source(bashrc_path)
# run_cmd('nvm install stable', con = True)
# run_cmd('npm install -g hexo-cli', con = True)


# ---Youcompleteme install---
welcome_print('Configing Youcompleteme')
ycm = user_path + '/' + '.vim/bundle/YouCompleteMe'
os.chdir(ycm)
run_cmd('git submodule update --init --recursive')
run_cmd('./install.py --clang-completer')
os.chdir(curr_path)
welcome_print('Config Youcompleteme success!')

error_log.close()

is_del_err_file = True
with open(error_log_file, 'r') as err:
    for line in err:
        if len(line.strip()) != 0:
            is_del_err_file = False

if is_del_err_file:
    run_cmd('rm -f ' + error_log_file)


welcome_print('All Config Complete!')
del_self()
