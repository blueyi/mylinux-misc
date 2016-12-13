#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <@BLUEYI-PC>
#
# Distributed under terms of the MIT license.

from common import *

"""
wget --no-check-certificate -r -p -np -k   https://developer.android.com/studio/intro/ -e use_proxy=yes -e https_proxy=127.0.0.1:1081
"""


https = True
proxy = True;
proxy = '127.0.0.1:1081'
url_file = 'url.txt'
down_dir = 'F:\\Download'
# error_log_file = 'wgetSite_error.log'


# error_log = open(error_log_file, 'w')

welcome_print('Make a mirror site by wget, powered by blueyi')

wget_cmd = 'wget -r -p -np -k '

if https :
    wget_cmd = wget_cmd + ' --no-check-certificate '

if proxy :
    wget_cmd = wget_cmd + ' -e use_proxy=yes -e https_proxy=' + proxy + ' '

if len(down_dir) != 0 :
    wget_cmd = wget_cmd + ' -P ' + down_dir + ' '

with open(url_file, 'r') as text:
    for tline in text:
        if len(tline.strip()) !=0 and 'http' in tline:
            tline = tline.strip()
            welcome_print('Downloading ' + tline)
            run_cmd_reout(wget_cmd + tline, goOnRun = True)


# error_log.close()
# 
# is_del_err_file = True
# with open(error_log_file, 'r') as err:
#     for line in err:
#         if len(line.strip()) != 0:
#             is_del_err_file = False
# 
# if is_del_err_file:
#     run_cmd_reout('rm -f ' + error_log_file, goOnRun=True)
# 

welcome_print('Download site Success!')


