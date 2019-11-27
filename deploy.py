#!/usr/bin/env python3

import os
import shutil


def make_local_bin():
    local_bin = os.path.join(os.environ['HOME'], '.local', 'bin')
    if not os.path.isdir(local_bin):
        os.mkdir(local_bin)
    return local_bin


def do_copy(from_, to_):
    for filep in os.listdir(from_):
        filep_src = os.path.join(from_, filep)
        filep_dst = os.path.join(to_, os.path.basename(filep))
        print('copy {} -> {}'.format(filep_src, filep_dst))
        shutil.copy(filep_src, filep_dst)


def main(dirp=None):
    if dirp is None:
        dirp = os.path.abspath('.')
    do_copy(os.path.join(dirp, 'src'), make_local_bin())


main()
