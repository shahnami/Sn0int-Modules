#!/bin/sh

#$(which python) export.py 9008&

$(which docker) run --rm --init -it --network=host -v $PWD/.cache:/cache -v $PWD/.data:/data kpcyrd/sn0int -w $1