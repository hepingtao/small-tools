#!/home/hepingtao/bin/anaconda3/envs/Py3.10/bin/python
# coding=utf-8
import sys

from login import login_interactive

if __name__ == '__main__':
    try:
        target_host_ip = sys.argv[1]
    except IndexError:
        print("No target given.")
        sys.exit(1)
    login_interactive(target_host_ip)
