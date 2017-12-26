#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
from datetime import datetime

if len(sys.argv) < 3:
    sys.exit("need more arguments")


source_dir = sys.argv[1]
target_dir = sys.argv[2]
temp_dir = os.path.join(target_dir, 'temp')
mask = sys.argv[3:]

if len(mask) == 0:
    mask.append("")


def copy_file(s_path, t_dir):
    """ copy source file to target directory"""
    if not os.path.exists(t_dir):
        os.makedirs(t_dir, exist_ok=True)
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

arch_name = datetime.strftime(datetime.now(), "%d.%m.%Y-%H:%M")
arch_path = target_dir + arch_name
shutil.make_archive(arch_name, 'zip', temp_dir)
