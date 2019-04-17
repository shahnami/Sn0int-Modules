#!/bin/sh

$(which python3) export.py $1 $2 $3&
$(which docker) run --rm --init -it --network=host -v $PWD/.cache:/cache -v $PWD/.data:/data kpcyrd/sn0int -w $2
PID=$($(which ps) -ef | $(which grep) -v grep | $(which grep) export.py | $(which awk) '{print $2}')
$(which kill) -9 $PID