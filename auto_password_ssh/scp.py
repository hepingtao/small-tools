#!/home/hepingtao/bin/anaconda3/envs/Py3.10/bin/python
# coding=utf-8
import sys

from login import scp

if __name__ == '__main__':
    scp_args = sys.argv[1:]
    if not scp_args:
        print("No arguments of scp command given.")
        sys.exit(1)
    scp(scp_args)
