#!/bin/perl
use strict;
#use DBI;
use File::Basename;
use constant VERSION => "V01.00.000";
#use Win32::Console::ANSI;
#use Term::ANSIColor;
#use IO::Tee;
use lib 'D:\hpt';
use perl_base::RemoteFun;

die("Usage: $0 <FtpType> <LocalPath/BaseFileName|[MatchGroup]> [RemotePath] [TransType]\n") if ($#ARGV < 1);

my ($FtpType, $LocalFullFileName, $RemotePath, $TransType) = @ARGV;

$LocalFullFileName =~ s/\\\./##/ig;
my ($BaseFileName, $LocalPath) = fileparse($LocalFullFileName);
$BaseFileName =~ s/##/\\\./ig;

#print "$LocalFullFileName, $LocalPath, $BaseFileName\n";

if(!$RemotePath)
{
    $RemotePath = "work/_hpt/";
}
elsif($RemotePath !~ m/^\//)
{
    $RemotePath = "work/_hpt/" . $RemotePath;
}

#$RemotePath = "debian";

my ($hostname, $username, $password) = ("172.20.32.96", 'etl', '123456');

my $oper;
if($FtpType =~ m/^put$/i)
{
    $FtpType = "PutTo";
    $oper = "From LocalHost:$LocalPath PutTo $hostname:$RemotePath successfullly!";
}
elsif($FtpType =~ m/^get$/i)
{
    $FtpType = "GetFrom";
    $oper = "From $hostname:$RemotePath GetTo LocalHost:$LocalPath successfullly!";
}
else
{
    print "FtpType error!\n";
    exit(-1)
}

print "#########ftp#########\n";
##ftp = FTP("172.20.32.96","etl","123456")
#my $nRet = ConnFtpHost("ftp.debian.org", 'anonymous', 'anonymous@');
my $nRet = ConnFtpHost($hostname, $username, $password);
if($nRet < 0)
{
    print "==oh no,,conn ftp error: $nRet\n";
    exit(-1);
}

SetBinaryFtp() if $TransType =~ m/^bin$/i;

CwdFtp($RemotePath);
#CwdFtp("debian");

print "Curr ftp dir ".PwdFtp()."\n";
#my @files = ();
#ListCurrDirFtp(\@files);
#
#foreach (@files)
#{
#    print "===$_\n";
#}


#my $FtpDir = PwdFtp();
print "$LocalPath, $BaseFileName\n";
my @result;
#GetFromFtp(PwdFtp(), $LocalPath, \@result, [$BaseFileName], 0);
my $FtpCmd = $FtpType . 'Ftp(PwdFtp(), $LocalPath, \@result, [$BaseFileName], 0)';
print "$FtpCmd\n";
eval $FtpCmd;
foreach (@result)
{
    print "+++ $_ $oper\n";
}

DisconnFtpHost();

