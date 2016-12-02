# -*- coding:utf-8 -*-

import sys, os
from ftplib import FTP

reload(sys)
sys.setdefaultencoding("utf-8")

#print len(sys.argv), sys.argv[0]
if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], "<FullFileName> <RemotePath> <TransType>"
    sys.exit(1)

def gettext(ftp, filename, outfile=None):
    # fetch a text file
    if outfile is None:
        outfile = sys.stdout
    # use a lambda to add newlines to the lines read from the server
    ftp.retrlines("RETR " + filename, lambda s, w=outfile.write: w(s+"\n"))

def getbinary(ftp, filename, outfile=None):
    # fetch a binary file
    if outfile is None:
        outfile = sys.stdout
    #ftp.retrbinary("RETR " + filename, outfile.write)
    ftp.retrbinary("RETR " + filename, outfile.write)

FullFileName = str(sys.argv[1])
file = open(FullFileName, "w")
try:
    RemotePath  = str(sys.argv[2])
    RemotePath  = "work/_hpt/" + RemotePath
except:
    RemotePath  = "work/_hpt/"

try:
    TransType     = str(sys.argv[3])
except:
    TransType     = "asc"
BaseFileName = os.path.basename(FullFileName)
LoaclPath    = os.path.dirname(FullFileName)

#print LoaclPath, RemotePath

GetOpr = {'asc':'gettext', 'bin':'getbinary'}
#ftp = FTP("172.20.32.96")
ftp = FTP("172.20.32.96","etl","123456")
#ftp.login("etl", "123456")
ftp.cwd(RemotePath)

#files = ftp.dir()
#print files

#gettext(ftp, BaseFileName, file)
#getbinary(ftp, BaseFileName, file)

Call = GetOpr[TransType] + "(ftp, BaseFileName, file)"
eval(Call)
