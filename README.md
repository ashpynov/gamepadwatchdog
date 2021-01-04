# Gamepad Watchdog

Set of script to 'pin' gamepads to specified Ports. 
It was designed and tested on next instalation:
1. RetroFlag Megapi cases 
1. Raspberry Pi3 B+ board
1. Two RetroFlag Wired Controller (Genesis style)
1. Batocera linux v29 OS

Batocera and Case was configured for safeshutdown usage (https://github.com/RetroFlag/Retroflag-picase/)

By default it pin:
* USB 1.2 device to input-Event #0 (Player #1 or Left USB port on case front panel)
* USB 1.3 device to input-Event #1 (Player #2 or Right USB port on case front panel)
* USB 1.0 device to input-Event #2 (Player #3 internal USB port)
* USB 1.1 device to input-Event #3 (Player #4 internal USB port)

# How to install on Batocera
Instalation is done and verified for Batocera version v29 and SHARED partition on microSD mounted into `/userdata/`

## Automatic via network
Network connection is required. Use wget as inspired by https://github.com/RetroFlag/retroflag-picase/)

Just copy and paste on Batocera ssh console:
```
wget -O - "https://raw.githubusercontent.com/ashpynov/gamepadwatchdog/main/batocera_install.sh" | bash
```

## Manually
Can be done via ssh or right on SHARE partition on microSD card (if you use microSD just know that /userdata/ is mounted as 'SHARE' partition )

1. Download files:
    1. `GamepadWatchdog.py`
    2. `99-gamepad_watchdog.rules`
    3. `custom.sh`
2. Put files into (create folders if needed):
    1. `GamepadWatchdog.py`  ->  `/userdata/RetroFlag/GamepadWatchdog.py`
    2. `99-gamepad_watchdog.rules`  ->  `/userdata/system/udev/rules.d/99-gamepad_watchdog.rules`
4. Modify/create `/userdata/system/custom.sh`:
    1. If file is already exist, put line from downloaded `custom.sh` at the end
    2. If file in not exist, just copy downloaded `custom.sh` there
5. Ensure that /userdata/system/custom.sh is executable: `chmod +x /userdata/system/custom.sh`
6. Execute `/userdata/system/custom.sh`

Here is the snippet:
```shell
    mkdir /userdata/RetroFlag/
    cp GamepadWatchdog.py /userdata/RetroFlag/GamepadWatchdog.py
    cp 99-gamepad_watchdog.rules /userdata/system/udev/rules.d/99-gamepad_watchdog.rules
    cat custom.sh >> /userdata/system/custom.sh
    chmod +x /userdata/system/custom.sh
    /userdata/system/custom.sh
```

# Usage on other platform / OS / cases
* It was NOT tested on any other Raspberry Pi models: but i suppose that it should be the same
* It was NOT tested on Recallbox: but it is very close to Batocera, so script should work, but instalation way may little differ
* It was NOT tested nither RetroPie nor Lakka: again it should work but have no idea how to install on it
* It was NOT tested with other cases, but it should work (may be except LED manipulation).


