#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import argparse
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', dest='source', 
                    type=str, required=True, 
                    help='source directory to backup'
                    )
parser.add_argument('-t', action='store', dest='target', 
                    type=str, required=True, 
                    help='target directory where backup will be created'
                    )
parser.add_argument('-e', action='store', nargs='*', dest='ext', 
                    type=str, default='', help='file masks to backup'
                    )
parser.add_argument('-a', action='store_true', dest='archive', 
                    default=False, help='make zip archive'
                    )
parser.add_argument('archname', 
                    nargs='?', 
                    default=datetime.strftime(
                               datetime.now(), 
                               "%d_%m_%Y-%H_%M"
                               ), 
                    help='name of the archive, default name \
                     "current date and time"')
args = parser.parse_args()


source_dir = args.source
target_dir = args.target
temp_dir = os.path.join(target_dir, 'temp')
mask = list(args.ext)
arch_name = args.archname
arch_path = os.path.join(target_dir, arch_name)

if not source_dir.endswith(os.sep):
    source_dir = source_dir + os.sep

if len(mask) == 0:
    mask.append('')
#else:
#    for ex in args.ext:
#        if ex.upper() not in mask:
#            mask.append(ex.upper())
#        if ex.lower() not in mask:
#            mask.append(ex.lower())

if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, mode=0o777, exist_ok=False)


def copy_file(s_path, t_dir):
    """ copy source file to target directory"""
    if not os.path.exists(t_dir):
        os.makedirs(t_dir, exist_ok=True)
        shutil.copy2(s_path, t_dir)
    else:
        shutil.copy2(s_path, t_dir)


def compare_date(s_path, t_path):
    """returns True if source file is newer"""
    s_date = os.stat(s_path).st_mtime
    t_date = os.stat(t_path).st_mtime
    return s_date > t_date


if os.path.isdir(source_dir):
    for root, dirs, files in os.walk(source_dir):
        for name in files:
            for ext in mask:
                if name.endswith(ext):
                    fullname = os.path.join(root, name)
                    s_path = fullname                    
                    t_path = os.path.normpath(os.path.join(temp_dir,
                            (fullname[len(source_dir):]))
                            )
                    t_dir = t_path[:-len(name)]
                    if not os.path.exists(t_path):
                        copy_file(s_path, t_dir)
                    else:
                        if compare_date(s_path, t_path):
                            copy_file(s_path, t_dir)
else:
    sys.exit("source dir does not exists")

if args.archive:
    shutil.make_archive(arch_path, 'zip', temp_dir)
