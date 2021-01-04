#!/bin/bash

SourcePath=https://raw.githubusercontent.com/ashpynov/gamepadwatchdog/main/

#-----------------------------------------------------------
sleep 2s

rules=/userdata/system/udev/rules.d/99-gamepad_watchdog.rules
wget -O  $rules "$SourcePath/99-gamepad_watchdog.rules"

#-----------------------------------------------------------
sleep 2s

mkdir /userdata/RetroFlag
script=/userdata/RetroFlag/GamepadWatchdog.py
wget -O  $script "$SourcePath/GamepadWatchdog.py"

#-----------------------------------------------------------

sleep 2s
DIR=/userdata/system/custom.sh

RUN="udevadm control --reload-rules; python $script refresh &"

if grep -q "$RUN" "$DIR";
	then
		if [ -x "$DIR" ];
			then 
				echo "Executable script already configured. Doing nothing."
			else
				chmod +x $DIR
		fi
	else
		echo "$RUN" >> $DIR
		chmod +x $DIR
		echo "Executable script configured."
fi
#-----------------------------------------------------------

echo "Gamepad watchdog script instalation done."
sleep 3
$DIR &

#-----------------------------------------------------------
