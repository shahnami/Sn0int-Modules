#!/bin/sh

$(which python3) export.py $1 $2 $3&
$(which python3) -m http.server 8000&

echo "[ * ] Started Listener Process"
echo "[ * ] Started HTTP Server"

if $4 
then
	echo "[ * ] Entering Interactive Shell"
	echo "[ * ] Modules should be placed in $HOME/Library/Application Support/sn0int/modules/"
	
	$(which ln) -s "$PWD/modules/shahnami/" "$HOME/Library/Application Support/sn0int/modules/" 2>/dev/null
	$(which sn0int) -w $2

else
	echo "[ * ] Entering Interactive Shell [Docker]"
	echo "[ * ] Modules should be placed in $PWD/.data/sn0int/modules/"
	
	$(which ln) -s "$PWD/modules/shahnami/" "$PWD/.data/sn0int/modules/" 2>/dev/null
	
	$(which docker) run --rm --init -it --network=host -v $PWD/.cache:/cache -v $PWD/.data:/data kpcyrd/sn0int -w $2
fi

PID=$($(which ps) -ef | $(which grep) -v grep | $(which grep) export.py | $(which awk) '{print $2}')
$(which kill) -9 $PID
echo "[ * ] Killed Listener Process"

PID=$($(which ps) -ef | $(which grep) -v grep | $(which grep) 8000 | $(which awk) '{print $2}')
$(which kill) -9 $PID
echo "[ * ] Killed HTTP Server"
