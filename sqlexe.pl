#!/usr/bin/perl
## FILENAME:sqlexe.pl
## PURPOSE: get table info and execute SQL statements
## AUTHOR:  He Pingtao
use strict;
use Encode;
use lib '/home/hector/lib';
#push(@INC, '/home/hector/lib');
#print @INC;
use HPT;
use constant VERSION => "V01.00.000"; #version ID

die("\nUsage: $0 [<TabNameStrs> <tab|desc|part|...>]|[SQL]\n\n") if ($#ARGV < 0);

my $dbtype;
$dbtype = splice(@ARGV,-1) if($ARGV[-1] =~ m/^db2$/i);

my $QueryType = splice(@ARGV,-1);
my ($TabName, $TabName2);
$TabName = uc(join('%', @ARGV)) if $QueryType =~ m/^tab$/i;
$TabName = $ARGV[0] if $QueryType !~ m/^tab$/i;
#print $TabName,"\n";
if($QueryType =~ m/^cp|cptab|cpdata$/i)
{
    $TabName2 = uc($ARGV[1]);
    #die "\nSource table is $TabName, but no object, please enter object table name follow source table\n\n" if(!$TabName2);
    $TabName2 = "DWHEPINGTAO" if(!$TabName2);
    #$TabName  = uc($TabName);
    $TabName =~ m/^([^\.\n]*)\.?([^\.\n]*)$/i;
    my ($TableSchema, $TableName) = ($1, $2);
    $TabName2 =~ m/^([^\.\n]*)\.?([^\.\n]*)$/i;
    my ($TableSchema2, $TableName2) = ($1, $2);
    my $ddl = HPT::GetOutPut($TabName, "ddl", $dbtype);
    if($TableSchema2 and !$TableName2)
    {
        $TabName2 = $TableSchema2 . "\." . $TableName;
    }
    $ddl =~ s/$TabName/$TabName2/gi;
    #print $ddl;
    #$ddl =~ s/\n//gm;
    my $rst;
    if($ddl)
    {
        print $ddl;
        #my $OutPut = HPT::GetOutPut($ddl, "none", $dbtype);
        $rst = Call($ddl, "none", $dbtype);
    }
    else
    {
        print "\nSource table $TabName is not exists! Please verify it!\n\n";
        exit(1)
    }

    if($QueryType =~ m/^cpdata$/i and $rst !~ m/fail/gmi)
    {
        my $insert = "insert into $TabName2 select * from $TabName"; 
        Call($insert, "none", $dbtype);
    }
}
else
{
    if(!$TabName)
    {
        $TabName = $QueryType;
        $QueryType = 5;
    }
    #print "$QueryType, $dbtype";
    #$TabName =~ s/--.*$//gm;
    #
    #my @TabName = split /\;/, $TabName;
    #@TabName = grep {$_ !~ m/^\s*$/g} @TabName;
    #
    #for $TabName(@TabName)
    #{
    #    #print $TabName,"\n";
    #    my $OutPut = HPT::GetOutPut($TabName, $QueryType, $dbtype);
    #    print $OutPut;
    #    print "---------------------------------------------------------------------------------------------------------------\n";
    #}
    
    my $rst = Call($TabName, $QueryType, $dbtype);
}

print "\n";

sub Call
{
   my ($TabName, $QueryType, $dbtype) = @_;

   $TabName =~ s/--.*$//gm;
   
   my @TabName = split /\;/, $TabName;
   @TabName = grep {$_ !~ m/^\s*$/g} @TabName;
   
   my $OutPut;
   for $TabName(@TabName)
   {
       #print $TabName,"\n";
       $OutPut = HPT::GetOutPut($TabName, $QueryType, $dbtype);
       #print encode('utf8', decode('gbk', $OutPut));
       #print from_to($OutPut, "gbk", "utf8");
       #print decode('gbk', $OutPut);
       print $OutPut;
       print "\n---------------------------------------------------------------------------------------------------------------\n";
   }

   #return $OutPut;
}

