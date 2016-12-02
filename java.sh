#!/bin/sh

if [ $# -le 0 ];then
    echo "Usage: $0 <CommandString>"
    exit 1
fi

echo "==================================================="

CommandString=$*
SCFileName=$1
ProgName=`echo ${SCFileName} | perl -pe 's/\.java$//g'`
ClassName="${ProgName}.class"

ArgID=0
for arg in $CommandString
do
    #echo $arg
    ArgID=`expr $ArgID + 1`
    if [ $ArgID -eq 1 ];then
        continue
    fi
    if [ -z "$Arguments" ];then
        Arguments="${arg}"
    else
        Arguments="${Arguments} ${arg}"
    fi
done

#PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\t \u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
if [ `echo $SCFileName | egrep -v ".java$"` ];then
    echo "\033[31mThe soure code file must follow suffix\033[m \033[01;05;31m.java\033[m \033[31m!\033[m"
    echo "==================================================="
    exit 1
elif [ ! -f ${SCFileName} ];then
    echo "\033[31mSource code file is not exists! Please ensure it!\033[m"
    echo "==================================================="
    exit 1
else
    echo "#Source code: ${CommandString}"
    echo "\033[32mSource code file name and arguments are OK!\033[m"
    echo "==================================================="
fi

echo "Start compiling: \033[33mjavac ${SCFileName}\033[m"
javac ${SCFileName}

if [ $? -eq 0 ] && [ -f ${ClassName} ];then
    echo "\033[32mCompiling OK!\033[m"
    echo "==================================================="
    echo "Start executing: \033[33mjava ${ProgName} ${Arguments}\033[m"
    echo "Output:"
    java ${ProgName} ${Arguments}
else
    echo "\033[31mCompiling fail! Class file failed to be generated!\033[m"
    echo "==================================================="
    exit 1
fi

if [ $? -ne 0 ];then
    echo "\033[31mRunning fail! Maybe you made some bugs just now!\033[m"
    echo "==================================================="
    exit 1
else
    echo "\033[32mExecuting OK!\033[m"
    echo "==================================================="
fi
