#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2014 Keita Kita
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
# Kill processes by name for Android
#

import argparse
import subprocess
import re


PROCESS_NAME_PATTERN = re.compile('^\S+\s+(?P<pid>\d+).+\s+(?P<name>.+)$')


def run_ps():
    return str(
        subprocess.check_output('adb shell ps', shell=True),
        encoding='utf-8')


def get_pid_list(process_name_list):
    pid_list = []
    is_header = True
    current_process_name_list = process_name_list[:]

    for process in run_ps().splitlines():
        if is_header:
            is_header = False
            continue
        if not process:
            continue

        match = PROCESS_NAME_PATTERN.match(process)

        for process_name in current_process_name_list[:]:
            if match.group('name') == process_name:
                pid_list.append(match.group('pid'))
                current_process_name_list.remove(process_name)

        if not current_process_name_list:
            break

    return pid_list


def run_kill(pid_list):
    if not pid_list:
        return

    subprocess.check_output(
        'adb shell kill -9 ' + ' '.join(pid_list), shell=True)


def kill(process_name_list):
    run_kill(get_pid_list(process_name_list))


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Kill processes by name for Android')
    parser.add_argument(
        'names', metavar='NAME', nargs='+', help='Process names')

    return parser


def kill_by_name_for_android():
    parser = create_argument_parser()
    arguments = parser.parse_args()

    kill(arguments.names)


if __name__ == '__main__':
    kill_by_name_for_android()
