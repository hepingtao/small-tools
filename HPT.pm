#!/usr/bin/perl

package HPT;
use strict;
use DBI;
use Term::ANSIColor;


#my $WorkingDir = "/home/etl/work/_hpt/bin";
#my $WorkingDir = "/etl1_cx/etl/work/_hpt/bin";
my $WorkingDir = "$ENV{HOME}/bin";
#chdir $WorkingDir;

#my %Query = ("tab"  => "TabName.sql",
#             "desc" => "TabDesc.sql",
#             "part" => "TabPart.sql"
#            );

my %Query = ("tab"      => "TabName",
             "desc"     => "TabDesc",
             "ddl"      => "TabDesc",
             "descddl"  => "TabDesc",
             "part"     => "TabPart"
            );

sub ConnDB
{
    my ($dbtype, $dbname, $username, $password) = @_;
    #my $conn = DBI->connect("DBI:Oracle:$dbname", $username, $password, { AutoCommit => 1, PrintError => 1, RaiseError => 1});
    #my $conn = DBI->connect("DBI:$dbtype:$dbname", $username, $password, {LongReadLen => 80000, AutoCommit => 1, PrintError => 1});
    my $conn = DBI->connect("DBI:$dbtype:$dbname", $username, $password, {LongReadLen => 1024 * 1024, AutoCommit => 1, PrintError => 1});

    return $conn;
}


sub ReadTabSql
{
    my ($SqlFile, $TableName) = @_;
    $TableName = $TableName . "\%" if $TableName =~ m/\.$/g;
    #print $TableName;
    my @TabName = split /\./, $TableName;
    my ($TabName, $TabSchema) = reverse(@TabName);
    die("Tablename is null!\n") if !$TabName;
    $TabSchema = "TabSchema" if(!$TabSchema);

    open FH, "< $SqlFile" || die "Can't open the file $SqlFile". $!;
    #print FH;
    my @SqlFile = <FH>;
    
    my $sql = join("", @SqlFile); 
    #print "Fuck";
    #print $SqlFile;
    #print @SqlFile;
    #print $sql;
    $sql =~ s/\$TabName/$TabName/g;
    $sql =~ s/\$TabSchema/$TabSchema/g;
    #print $sql;
    #exit(1);

    return $sql;
}

sub ConSql
{
    my ($dbtype, $TableName, $QueryType) = @_;
    my $sql;
    if($QueryType =~ m/^[0-9]+$/g)
    {
        my $rows = $QueryType;

        if($TableName =~ m/^\s*(select)\s+.*$/igs)
        {
            $sql = $TableName;

            if($dbtype eq "Oracle" and $sql !~ m/count|min|max\s*\(/is and $sql !~ m/distinct\s+/is and $sql !~ m/group\s+by/is)
            {
                if($sql !~ m/where\s+/is and $sql !~ m/\s+rownum/is and $sql !~ m/\s+order\s+by/is)
                {
                    $sql = $sql . "\n where rownum <= $rows";
                }
                elsif($sql !~ m/where\s+/is and $sql !~ m/\s+rownum/is and $sql =~ m/\s+order\s+by/is)
                {
                    $sql =~ s/(order\s+by.*$)//is;
                    $sql = $sql . "\n where rownum <= $rows $1";
                }
                elsif($sql =~ m/where\s+/is and $sql !~ m/\s+rownum/is and $sql !~ m/\s+order\s+by/is)
                {
                     $sql = $sql . "\n and rownum <= $rows";
                }
                elsif($sql =~ m/where\s+/is and $sql !~ m/\s+rownum/is and $sql =~ m/\s+order\s+by/is)
                {
                     $sql =~ s/(order\s+by.*$)//is;
                     $sql = $sql . "\n and rownum <= $rows $1";
                }
            }

            if($dbtype eq "DB2" and $sql !~ m/count|min|max\s*\(/is and $sql !~ m/distinct\s+/is and $sql !~ m/group\s+by/is)
            {
                if($sql !~ m/\s+fetch/is and $sql !~ m/\s+order\s+by/is)
                {
                    $sql = $sql . "\n fetch first $rows rows only";
                }
                elsif($sql !~ m/\s+fetch/is and $sql =~ m/\s+order\s+by/is)
                {
                    $sql =~ s/(order\s+by.*$)//is;
                    $sql = $sql . "\n fetch first $rows rows only $1";
                }
            }
        }
        else
        {
            #$sql = "select * from $TableName where rownum <= $rows";
            if($dbtype eq "Oracle")
            {
                $sql = "select * from $TableName where rownum <= $rows";
            }
            elsif($dbtype eq "DB2")
            {
                $sql = "select * from $TableName fetch first $rows rows only with ur";
            }
            else
            {
                print "DBtype is wrong!";
                exit(1)
            }
        }
    }
    elsif($QueryType =~ m/^count$/i)
    {
        $sql = "select count(*) from $TableName t";
    }
    elsif($QueryType =~ m/^delete$/i)
    {
        $sql = "delete from $TableName";
    }
    elsif($QueryType =~ m/^drop$/i)
    {
        $sql = "drop table $TableName purge";
    }
    elsif($QueryType =~ m/^truncate$/i)
    {
        $sql = "truncate table $TableName";
    }
    elsif($QueryType =~ m/^(none)$/i)
    {
        $sql = $TableName;
        $sql =~ s/^ +//g;
        $sql =~ s/ +$//g;
    }
    elsif($QueryType =~ m/^(txt|sql)$/i)
    {
        if($TableName =~ m/^\s*(select)\s+.*$/is)
        {
            $sql = $TableName;
            $sql =~ s/^ +//g;
            $sql =~ s/ +$//g;
        }
        else
        {
            $sql = "select * from $TableName";
        }
    }
    else
    {
       print "\nI don't konw what will I do that you want! Please tell me clearly!\n\n";
       exit 1;
    }
    #chomp($sql);

    return $sql;
}

sub GetSql
{
    my ($TableName, $QueryType, $dbtype) = @_;

    #print $QueryType,"\n";
    my $sql;
    if($QueryType =~ m/^(tab|desc|ddl|descddl|part)$/ig)
    {
       my $SqlFile = "$WorkingDir/$Query{$QueryType}$dbtype\.sql";
       $sql = ReadTabSql($SqlFile, $TableName);
       #print $SqlFile;
       #print $sql;
       #exit(1);
    }
    else
    {
       $sql = ConSql($dbtype, $TableName, $QueryType);
    }
    #print $sql;
    #exit(1);
    $sql =~ s/--.*$//gm;
    $sql =~ s/\s+$//gm;
    $sql =~ s/\s+,/,/g;
    $sql =~ s/, +$/,/gm;

    return $sql;
}


sub GetHeader
{
    my ($conn, $sql, $dbtype, $QueryType) = @_;
    #print $sql;
    my @Header;
    $sql =~ m/^\s*(with)*\s*.*?select\s+(.*?)\s+from\s+(\S+)\s*.*$/igs;
    #print $1;
    my $cols = $2;
    my $TabName = uc($3);
    #print $TabName;
    chomp($TabName);
    
    chomp($cols);
    $cols =~ s/--.*$//gm;
    $cols =~ s/\s+$//gm;
    $cols =~ s/\s+,/,/g;
    $cols =~ s/, +$/,/gm;
    $cols = $cols . ",\n";
    $cols =~ s/,\n/, /gm;
    $cols =~ s/,/, /gm;
    $cols =~ s/(\|\|\s*'\s*,)\s+('\s*\|\|)/$1$2/gm;
    #$cols =~ s/(\w[^\(].*),/$1, /gm;
    #print $cols,"\n";
    #$cols =~ s/'\|\|t2.DATA_LENGTH\|\|'/'\|\|t2.DATA_LENGTH\|\|'/m;
    #print $cols,"\n";
    #exit;
    my @brace;
    #@brace = ($cols =~ m/\((.*?)\)/gm);
    if($cols =~ m/[\)]{2,}/)
    {
        @brace = ($cols =~ m/\((.*?)\)\s+/gm);
    }
    else
    {
        #@brace = ($cols =~ m/\((.*?)\)/gm);
        @brace = ($cols =~ m/\((.*?)\)/gm);
    }
    #print "\n$#brace";
    for (@brace)
    {
        my $old= $_;
        $_ =~ s/\s+//g;
        my $new = $_;
        $old =~ s/\//\\\//g;
        $old =~ s/\|/\\|/g;
        $old =~ s/\+/\\+/g;
        #$new =~ s/\|/\\|/g;
        $old =~ s/\*/\\*/g;
        $old =~ s/\(/\\(/g;
        $old =~ s/\)/\\)/g;
        $old =~ s/\$/\\\$/g;
        #$new =~ s/\*/\\*/g;
        #print "$old, $new\n\n";
        $cols  =~ s/$old/$new/m;
        #print $cols,"\n\n";
        #exit
    }
    #print $cols;
    my @col = split / +/, $cols;
    @col = map { $_ =~ s/,$/,\n/g; $_ } @col;
    #@Header = map { $_ =~ s/,\n//g; chomp($_); $_ } grep { $_ =~ m/^[a-zA-Z0-9\.]+(\(.*\)|\S*),\n$/g } @col;
    @Header = map { $_ =~ s/,\n//g; chomp($_); $_ } grep { $_ =~ m/^[\S]+,\n$/g } @col;
    #map {print length($_),"\n"} @Header;
    #print $Header[0],"\n";

    if($#Header == 0 and $Header[0] =~ m/^\*$/g)
    {
        my $sql = GetSql($TabName, "desc", $dbtype);
        #print $sql, $TabName, $dbtype;
        #exit(1);
        my @TabStructure = GetSqlQuery($conn, $sql);
        @Header = @{$TabStructure[3]} if @TabStructure;
    }

    return @Header;
}


sub GetSqlQuery
{
    my ($conn, $sql) = @_;
    #print $sql;
    #exit(1);
    my $sth = $conn->prepare($sql);
    $sth->execute() || die "Can't execute the query! $sth->errstr";
    #$sth->execute();

    my @SqlQuery;
    while(my @row = $sth->fetchrow_array())
    {
        for my $ColID(0..$#row)
        {
            my $ColValue = $row[$ColID];
            #print $ColValue," ";
            push @{$SqlQuery[$ColID]}, $ColValue;
        }
        #print "\n";
    }

    return @SqlQuery;
}


sub GetSqlNonQuery
{
    my ($conn, $sql) = @_;
    my $SqlNonQuery = $conn->do($sql);
    # || die "Can't execute the operation!";

    return $SqlNonQuery;
}


sub GetTabKey
{
    my ($conn, $TabName, $dbtype) = @_;
    $dbtype = "DB2"    if $dbtype =~ /^db2$/i;
    $dbtype = "Oracle" if $dbtype !~ /^db2$/i;
    #print $dbtype;
    #exit;

    ##DB connecting information
    #my ($dbname, $username, $password) = ("biwg", "etl", "etl");
    #my ($dbname, $username, $password) = ("wgods", "dwhepingtao", "hepingtao_wgods_123");
    #Oracle
    my ($dbname, $username, $password);
    ##Oracle
    ($dbname, $username, $password) = ("wgods", "etl", "wgods_etl_123") if $dbtype eq "Oracle";
    #($dbname, $username, $password) = ("biwg", "etl", "etl") if $dbtype eq "Oracle";
    ##DB2
    ($dbname, $username, $password) = ("dbctl2", "etl", "wgods@#\$") if $dbtype eq "DB2";
    #($dbname, $username, $password) = ("dbctl", "etl", "123456") if $dbtype eq "DB2";
    
    my $conn = ConnDB($dbtype, $dbname, $username, $password);
    
    my $msg;
    if (!defined($conn))
    {
       $msg = "DBI connect failed (dbname=$dbname). " . DBI->errstr;
       die $msg;
    }
    else
    {
       $msg = "DBI connect succeeded (dbname=$dbname). ";
    }
    $dbtype = "Oracle" if !$dbtype;
    my $sql = GetSql($TabName, "desc", $dbtype);
    my @TabStructure = GetSqlQuery($conn, $sql);
    my %TabCol;
    my $Rows = @{$TabStructure[0]};
    #print $Rows,"\n";

    for my $ColID(0..$Rows - 1)
    {
        my $ColName = $TabStructure[3]->[$ColID];
        #print $ColName;
        $TabCol{$ColName} = $ColID;
    }
    #my @KeyCol = @{$TabStructure[7]};
    #print $#KeyCol,"\n";
    my @KeyCols = grep { $_ ne "" } @{$TabStructure[7]};
    #print @KeyCols,"\n";

    my @TabKey;
    for my $ColName(@KeyCols)
    {
        my $ColID = $TabCol{$ColName};
        my @row = ($ColID, $ColName);
        #print @row,"\n";
        for my $KeyColID(0..$#row)
        {
            push @{$TabKey[$KeyColID]}, $row[$KeyColID];
        }
    }

    return @TabKey;
}


sub GetOutPut
{
    my ($TabName, $QueryType, $dbtype) = @_;
    $dbtype = "DB2"    if $dbtype =~ /^db2$/i;
    $dbtype = "Oracle" if $dbtype !~ /^db2$/i;
    #print $dbtype;
    #exit;

    ##DB connecting information
    #my ($dbname, $username, $password) = ("biwg", "etl", "etl");
    #my ($dbname, $username, $password) = ("wgods", "dwhepingtao", "hepingtao_wgods_123");
    #Oracle
    my ($dbname, $username, $password);
    ##Oracle
    #($dbname, $username, $password) = ("wgods", "etl", "wgods_etl_123") if $dbtype eq "Oracle";
    ($dbname, $username, $password) = ("BILEARN", "frnt", "frnt") if $dbtype eq "Oracle";
    #($dbname, $username, $password) = ("biwg", "etl", "etl") if $dbtype eq "Oracle";
    ##DB2
    ($dbname, $username, $password) = ("dbctl2", "etl", "wgods@#\$") if $dbtype eq "DB2";
    #($dbname, $username, $password) = ("dbctl", "etl", "123456") if $dbtype eq "DB2";
    
    my $conn = ConnDB($dbtype, $dbname, $username, $password);
    #print "fuck?\n";
    
    my $msg;
    if (!defined($conn))
    {
       $msg = "DBI connect failed (dbname=$dbname). " . DBI->errstr;
       die $msg;
    }
    else
    {
       $msg = "DBI connect succeeded (dbname=$dbname). ";
    }

    my $TableExist = 0;
    #print $TabName,"\n";
    $QueryType = "none" if $TabName =~ m/^\s*(create|alter|rename|comment|insert|update|delete|truncate|drop|commit)\s*.*$/is;
    my $sql = GetSql($TabName, $QueryType, $dbtype);
    #print "$QueryType\n";
    #print "\n$sql;\n";
    print "\n$sql;\n" if $QueryType !~ m/^(tab|desc|part|ddl|descddl)$/i;

    $sql =~ m/^\s*(\S+)\s+.*$/igs;

    my $OutPut = "\n";
    my $title;
    my $body;

    my $DDL;
    my $DDLHeader = "\n--DDL\n";
    my $TabDesc;
    my $DropSt;
    my $CreateSt;
    my $Cols = "(\n";
    my $PTCol;
    my $PTAddSt;
    my $Separator = ";\n\n";
    my $PKCols;
    my $PKAddSt;
    my $TabCommAddSt;
    my $ColCommAddSt;

    my $oper = uc($1);
    #print $oper;
    #exit;

    if($oper =~ m/select|with/ig)
    {
        #print $sql;
        #exit(1);
        my @Header = GetHeader($conn, $sql, $dbtype, $QueryType);
        #print $sql;
        my @SqlQuery = GetSqlQuery($conn, $sql);
        #print @SqlQuery;
        my ($allrows, $firstrows, $morerows) = (0, 0, 0);
        $allrows = @{$SqlQuery[0]} if @SqlQuery;
        $morerows = $allrows - 100;

        $sql =~ m/^\s*select\s+(.*?)\s+from\s+(\S+)\s*.*$/is;
        #print "$1,$2";
        my $SqlTabName = uc($2);
        chomp($SqlTabName);

        my $SqlDataType;
        my @TabStructure;
        my %DataType;
        if($QueryType =~ m/^(sql|txt)$/i)
        {
            $SqlDataType = GetSql($SqlTabName, "desc", $dbtype);
            @TabStructure = GetSqlQuery($conn, $SqlDataType);

            if(@TabStructure)
            {
                my $Cols;
                $Cols = $#{$TabStructure[3]} if @TabStructure;
                #print $#{$TabStructure[3]};
                #$Cols = @{$TabStructure[3]} - 1 if @TabStructure;
                #print $Cols;
                for my $ColID(0..$Cols)
                {
                    my $ColName = $TabStructure[3]->[$ColID];
                    my $DataType= $TabStructure[4]->[$ColID];
                    $DataType{$ColName} = $DataType;
                }
            }
        }

        my ($del, $OutFile) = (" ", "sqlexe.data");
        if($QueryType =~ m/^(txt|sql)$/i)
        {
            $del = ",";
            $OutFile = "$SqlTabName.$QueryType";
        }
        unlink $OutFile;

        my ($TabPhyName, $TabLogName);
        if($QueryType =~ m/^(desc|ddl|descddl)$/i)
        {
           splice(@Header, 0, 2);
           my @TableName = splice(@SqlQuery, 0, 2);
           if(@TableName)
           {
               $TableExist = 1; 
               ($TabPhyName, $TabLogName) = ($TableName[0]->[0], $TableName[1]->[0]);
               $title = "TableName:    $TabPhyName        $TabLogName\n\n";
               $TabDesc = "----TableName:    $TabPhyName        $TabLogName\n";
               $DropSt = "DROP TABLE $TabPhyName PURGE;\n";
               $CreateSt = "CREATE TABLE $TabPhyName\n";
               $TabCommAddSt = "COMMENT ON TABLE $TabPhyName IS '$TabLogName';\n";
           }
        }

        if($QueryType !~ m/^sql$/i)
        {
            for my $ColID(0..$#Header)
            {
                unshift @{$SqlQuery[$ColID]}, $Header[$ColID];
            }
        }

        my @Lines = @{$SqlQuery[0]} if @SqlQuery;
        for my $LineID(0..$#Lines)
        {
            my $SepLine;
            my $tmpbody;
            my ($insert, $over);

            for my $ColID(0..$#SqlQuery)
            {
                #if
                my $MaxColLen = (sort {$a <=> $b} map {length($_)} @{$SqlQuery[$ColID]})[-1];
                #print $MaxColLen,"\n";
                my $CurColName = $SqlQuery[$ColID]->[$LineID];

                chomp($CurColName);
                ##Trim nulls
                $CurColName =~ s/^ +//g;
                $CurColName =~ s/ +$//g;

                my $CurColLen = length($CurColName);
                if($QueryType =~ m/^(txt|sql)$/i)
                {
                    my $HeaderType = $DataType{$Header[$ColID]};
                    if($QueryType =~ m/^(sql)$/i)
                    {
                        my $Header = join ', ', @Header;
                        $CurColName = "NULL" if $CurColName =~ m/^$/;
                        $CurColName = "\'$CurColName\'" if($HeaderType =~ m/char/i and $CurColName ne "NULL");
                        $insert = "insert into $SqlTabName ($Header)\nvalues (";
                        $over = ");";
                    }
                    elsif($QueryType =~ m/^(txt)$/i)
                    {
                        #print $HeaderType;
                        $CurColName = "\"$CurColName\"" if($HeaderType =~ m/char/i);
                        #print $CurColName;
                        #exit;
                    }
                }
                else
                {
                    if($CurColLen < $MaxColLen)
                    {
                        my $DiffLen = $MaxColLen - $CurColLen;
                        $CurColName = $CurColName . " " x $DiffLen;
                    }
                }

                $tmpbody = $tmpbody . $del . $CurColName if $tmpbody;
                $tmpbody = $insert . $CurColName if !$tmpbody;

                if($LineID == 0)
                {
                    my $CurLine = "-" x $MaxColLen;
                    $SepLine = $SepLine . $del . $CurLine if $SepLine;
                    $SepLine = $CurLine if !$SepLine;
                }

                if($QueryType =~ m/^(ddl|descddl)$/i and $LineID > 0)
                {
                    if($ColID =~ m/1|2|3/i)
                    {
                        if($ColID == 3)
                        {
                            $CurColName =~ s/N +/NOT NULL/g;
                            $CurColName =~ s/Y +//g;
                        }

                        if($LineID > 1 and $ColID == 1)
                        {
                            $Cols = $Cols . '      ,' . $CurColName;
                        }
                        else
                        {
                            $Cols = $Cols . '       ' . $CurColName;
                        }
                        $Cols = $Cols . "\n" if $ColID == 3;
                    }

                    if($ColID == 5 and $CurColName !~ m/^\s*$/)
                    {
                        #print "yes\n";
                        #exit;
                        $CurColName =~ s/\s+$//;
                        $CurColName =~ s/^\s+//;
                        #print $CurColName,"\n";
                        if($PKCols eq "")
                        {
                            $PKCols = $CurColName;
                        }
                        else
                        {
                            $PKCols = $PKCols . ', ' . $CurColName;
                        }
                    }

                    if($ColID == 6 and $CurColName !~ m/^\s*$/ig)
                    {
                        $CurColName =~ s/\s+$//;
                        $CurColName =~ s/^\s+//;
                        if($PTCol eq "")
                        {
                            $PTCol = $CurColName;
                        }
                        else
                        {
                            $PTCol = $PTCol . ', ' . $CurColName;
                        }
                    }

                    if($ColID =~ m/1|4/i)
                    {
                        $ColCommAddSt = $ColCommAddSt . "COMMENT ON COLUMN $TabPhyName\." . $CurColName if $ColID == 1;
                        if($ColID == 4)
                        {
                            $CurColName =~ s/ +$//;
                            $ColCommAddSt = $ColCommAddSt . " IS " . "'$CurColName';";
                        }
                        $ColCommAddSt = $ColCommAddSt . "\n" if $ColID == 4;
                    }
                }

            }

            $tmpbody = $tmpbody . $over if $insert;
            $LineID = $LineID + 1 if $QueryType =~ m/^(sql)$/i;
            my $CommitLineID = $LineID % 100;
            $tmpbody = $tmpbody . "\ncommit;" if($insert and $CommitLineID == 0);
            $tmpbody = $tmpbody . "\ncommit;" if($insert and $LineID == $allrows and $CommitLineID != 0);
            if($QueryType =~ m/desc/i)
            {
                $body = $body . "\n" . $tmpbody if $body;
                $body = $tmpbody if !$body;
                $body = $body . "\n" . $SepLine if($LineID == 0);
                $firstrows = $LineID;
            }
            else
            {
                if($LineID <= 100)
                {
                    $body = $body . "\n" . $tmpbody if $body;
                    $body = $tmpbody if !$body;
                    $body = $body . "\n" . $SepLine if($LineID == 0 and $QueryType !~ m/^(txt|sql)$/i);
                    $firstrows = $LineID;
                }
                else
                {
                    my $firstbody = $body;
                    open DATA, ">> $OutFile" || die "Can't open the file " . $!;
                    print DATA $firstbody if($firstbody and $LineID == 101);
                    print DATA "\n" . $tmpbody;
                    print DATA "\n" if $LineID == $allrows;
                }
            }
        }

        $Cols = $Cols . ")\n";
        #print $PKCols;

        if($PTCol)
        {
            $PTAddSt = "PARTITION BY LIST ($PTCol)\n(\n    PARTITION PART20140101 VALUES (20140101)\n)\n";
        }
        
        if($PKCols)
        {
            $PKAddSt = "ALTER TABLE $TabPhyName ADD PRIMARY KEY ($PKCols);\n\n";
        }

        $body = $body . "\n";
        $OutPut = $OutPut . $title . $body . "\n";
        $OutPut = $OutPut . "    $firstrows rows selected.\n";
        $OutPut = $OutPut . "    all $allrows rows seen in $OutFile\n" if $morerows >= 1 and $QueryType !~ m/^desc$/i;
    }
    else
    {
        my $SqlNonQuery = GetSqlNonQuery($conn, $sql);
        my $rst;
        if($oper =~ m/^(insert|delete|update)$/ig and $SqlNonQuery =~ m/^[0-9]+$/i)
        {
            $rst = " rows have been done! Perfectly!\n";
            $OutPut = $OutPut . "$oper: " . $SqlNonQuery . $rst;
        }
        elsif($SqlNonQuery eq "0E0")
        {
            $rst = "have been done! Perfectly!\n";
            $OutPut = $OutPut . "$oper: " . $rst;
        }
        elsif($oper =~ m/^(drop)$/i)
        {
            $rst = "have failed! Sorry! Maybe it's not exists!\n";
            $OutPut = $OutPut . "$oper: " . $rst;
        }
        else
        {
            $rst = "have failed! Sorry! Please check it!\n\n";
            print color 'bold red';
            print $OutPut . "$oper: " . $rst;
            print color 'reset';
            print "---------------------------------------------------------------------------------------------------------------\n\n";
            exit 1;
        }
    }
    
    my $OutPut = $OutPut . "\n";
    if($QueryType =~ m/^ddl|descddl$/i)
    {
        $DDL = $DDLHeader . $TabDesc . $DropSt . $CreateSt . $Cols . $PTAddSt . $Separator . $PKAddSt . $TabCommAddSt . $ColCommAddSt if $TableExist;
        $OutPut = $DDL if $QueryType =~ m/^ddl$/i;
    }

    if($QueryType =~ m/^descddl$/i)
    {
        $OutPut = $OutPut . $DDL;
    }

    #$OutPut = $OutPut . "\n";

    return $OutPut;
}

1;
