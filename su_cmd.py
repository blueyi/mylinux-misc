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


error_log_file = 'su_install_err.log'
error_log = open(error_log_file, 'w')


def print_to_file(msg, file_opened=error_log):
    print(msg)
    file_opened.write(str(msg) + '\n')

def run_cmd(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    returncode = subprocess.call(tcall_cmd, shell=True, executable = '/bin/bash')
    if returncode != 0 and ('grep' not in tcall_cmd):
        if os.geteuid() != 0:
            print_to_file('Please run the script by "root"!')
            sys.exit(1)
        print_to_file('<<< ' + tcall_cmd + '>>> run failed!')
        if not con :
            sys.exit(1)
    return returncode



def run_cmd_reout(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable = '/bin/bash')
    toutput = p.communicate()[0]
    if p.returncode != 0 and ('grep' not in tcall_cmd):
        if os.geteuid() != 0:
            print_to_file('Please run the script by "root"!')
            sys.exit(1)
        print_to_file('<<< ' + tcall_cmd + '>>> run failed!')
        print_to_file(toutput)
        if not con :
            sys.exit(1)
    print(toutput)
    return toutput


def first_run_fail(msg):
    print_to_file('System info:')
    for item in platform.uname():
        print_to_file(item)
    print_to_file(msg)
    del_self()
    sys.exit(1)


if os.geteuid() != 0:
    first_run_fail('Please run the script by "root"!')

# if platform.machine().lower() != 'x86_64':
#    first_run_fail('This script only support x86_64 system, please contact getworld@qq.com')


# Current path
curr_path = os.path.split(os.path.realpath(__file__))[0]

install_cmd = None
dis_cmd = None
soft_list_file = None
if is_list_in_str(apt_list, sys_distribution):
    install_cmd = 'apt-get install '
    dis_cmd = 'apt'
    soft_list_file = 'deb_app_list.json'
    run_cmd('apt-get update -y')
elif is_list_in_str(rpm_list, sys_distribution):
    install_cmd = 'yum install '
    dis_cmd = 'yum'
    soft_list_file = 'rpm_app_list.json'
    run_cmd('yum update -y')
else:
    first_run_fail('Your distribution not in supported list, please contact getworld@qq.com')

soft_list_file = curr_path + '/' + soft_list_file


def package_query_cmd(soft):
    package_query_str = ''
    if dis_cmd == 'apt':
        package_query_str = "dpkg --get-selections | grep '\\b" + soft + "\\s*install'"
    elif dis_cmd == 'yum':
        package_query_str = "rpm -qa | grep '\\b" + soft + "'"
    return package_query_str


def depend_install(soft):
    toutput = run_cmd(package_query_cmd(soft))
    if soft in toutput.__str__():
        print(soft,  '-- You have installed!')
    print('---Installing ' + soft + ' ---')
    run_cmd(install_cmd, soft + ' -y', con = True)

soft_list = []
with open(soft_list_file, 'r') as text:
    for tline in text:
        if tline[0] != '#' and len(tline.strip()) != 0:
            soft_list.append(tline.strip().split('#')[0])

welcome_print('You have ' + len(soft_list).__str__()  + 'softwares need to be install')
for app in soft_list:
    depend_install(app)


# ---Other dependence install---
# ---CentOS epel install---
def epel_url(ver_num=7, mac='x86_64'):
    if ver_num < 7:
        if mac == 'i686':
            mac = 'i386'
            url = 'dl.fedoraproject.org/pub/epel/' + str(ver_num) + '/' + mac + '/'
        else:
            url = 'dl.fedoraproject.org/pub/epel/' + str(ver_num) + '/' + mac + '/' 
    else:
        url = 'dl.fedoraproject.org/pub/epel/' + str(ver_num) + '/' \
                + mac + '/e/'
    return url


def centos_ver():
    t_os_ver_num = 7
    tout = run_cmd_reout('cat /etc/centos-release ')
    tlist = tout.split()
    for word in tlist:
        if word[0].isdigit():
            t_os_ver_num = int(word[0])
    return t_os_ver_num
 

def ubuntu_ver():
    t_os_ver_num = 14
    tout = run_cmd_reout('lsb_release -r')
    tlist = tout.split()
    for word in tlist:
        if word[0].isdigit():
            t_os_ver_num = float(word)
    return t_os_ver_num


# install epel
if dis_cmd == 'yum':
    if 'centos' in sys_distribution:
        os_ver_num = centos_ver()
        machine = platform.machine()
        tepel = epel_url(os_ver_num, machine)
        output = run_cmd(package_query_cmd("epel-release-*"))
        if 'epel' not in output.__str__():
            t_cmd = "wget -r --no-parent -A 'epel-release-*.rpm' http://" + tepel
            run_cmd(t_cmd)
            t_cmd = "rpm -Uvh " + tepel + "epel-release-*.rpm"
            run_cmd(t_cmd)
            run_cmd('rm -rf dl.fedoraproject.org')
        run_cmd('yum update -y')


#  ---install supervisor---
# supervisord install in centos 6
def centos6_install_supervisord():
    run_cmd('yum install python-setuptools -y')
    run_cmd('easy_install supervisor')
    down_su_init = 'https://bitbucket.org/getworld/ss_go_mu_getworld_server/raw/master/supervisord'
    down_su_init_cmd = 'wget -O /etc/rc.d/init.d/supervisord ' + down_su_init
    down_su_conf = 'https://bitbucket.org/getworld/ss_go_mu_getworld_server/raw/master/supervisord.conf'
    down_su_conf_cmd = 'wget -O /etc/supervisord.conf ' + down_su_conf
    run_cmd(down_su_init_cmd)
    run_cmd(down_su_conf_cmd)
    run_cmd('chmod 755 /etc/rc.d/init.d/supervisord')
    run_cmd('chkconfig --add supervisord')
    run_cmd('chkconfig supervisord on')


# Install supervisor and auto start ss-go
def supervisor_install():
    supervisor_log_path = '/var/log/supervisor/'
    if not os.path.exists(supervisor_log_path):
        run_cmd('mkdir -p ' + supervisor_log_path)
    if dis_cmd == 'apt':
        depend_install('supervisor')
        ubuntu_su_conf_path = '/etc/supervisor/conf.d/'
        if not os.path.exists(ubuntu_su_conf_path):
            run_cmd('mkdir -p ' + ubuntu_su_conf_path)
        if ubuntu_ver() > 16.0:
            run_cmd('systemctl enable supervisor.service')
        run_cmd('service supervisor restart')
    elif dis_cmd == 'yum':
        centos_su_conf_path = '/etc/supervisord.d/'
        if not os.path.exists(centos_su_conf_path):
            run_cmd('mkdir -p ' + centos_su_conf_path)
        if centos_ver() < 7:
            centos6_install_supervisord()
            run_cmd('service supervisord restart')
        else:
            depend_install('supervisor')
            run_cmd('systemctl start supervisord.service')
            run_cmd('systemctl enable supervisord.service')

# supervisor_install()


# ---Create soft link for config file---
welcome_print('Linking global config file')
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
            if tline[0] != '#' and len(tline.strip()) != 0 and 'home' not in tline:
                tlink = tline.strip().split('#')[0].split()
                if len(tlink) > 1:
                    link_dict[tlink[0]] = tlink[1]
    for key, value in link_dict.items():
        if os.path.isfile(value):
            run_cmd('mv ' + value + ' ' + value + '.bak')
        run_cmd(link_cmd(curr_path + '/' + key, value), con = True)

config_link(config_link_file)

welcome_print('Linking global config file success!')


welcome_print('supervisor status')
#run_cmd('service supervisor start')
run_cmd('supervisorctl reload')
#run_cmd('supervisorctl status')

error_log.close()

is_del_err_file = True
with open(error_log_file, 'r') as err:
    for line in err:
        if len(line.strip()) != 0:
            is_del_err_file = False

if is_del_err_file:
    run_cmd('rm -f ' + error_log_file)


welcome_print('Install Success!')
del_self()
