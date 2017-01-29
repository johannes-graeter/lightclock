# Lightclock

Code for realizing a fading light clock on a micropython capable board.
Tested with HUZZAH ESP8266 Feather.

## Installation

* Install micropython on board <https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html> until point 1.5
* play with the board using picocom: 
>sudo picocom /dev/ttyUSB0 -b 115200

* log onto board with picicom and enable webREPL: `import webrepl_setup`
* log off
* download webrepl from github https://github.com/micropython/webrepl.git and start firefox webrepl.html

Copy files:
1. Offline:
    * install ampy: `sudo pip2 install adafruit-ampy`
    * use ampy to put the files on the board as described here
    https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy


2. Online 
    * copy files with webrepl via accesspoint
    * The accesspoint didn't work for me

* You will need the following files under the same filenames intpo the root directory on the board:
    * `commons/boot.py`
    * `commons/connect_to_router.py`
    * `lightclock/alarm.py`
    * `lightclock/clock_actions_micropython.py`
    * `lightclock/main.py`
    * `lightclock/config.json`
    * `lightclock/alarmtime.json`
* You will need to configure your private configs. Therefore put the following files into your root directory:
    * `config_wifi.json` where you put the data of your network in the following format, static_ip is the ip which the controller will have at startup:
        ```json
         {
            "ssid": "my_home_network_ssid",
            "password": "my_password",
            "static_ip": "my_chosen_static_ip_for_board"
        }   
        ```
* branch off an on, main will start on boot
* Now you can communicate with your board via webrepl, connecting to the static_ip configured


## Usage

Offline:
* plugin your usb cable and modify config.json and alarmtime.json

Online:
* set up static IP on your router

EITHER: 
* Send file using WebRepl <http://micropython.org/webrepl/>

OR:
* access the html interface to modfiy the configs (not yet implemented)

## Sources

    * https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl

## Todo

* Test on micro-controller
* html interface - only server and trigger when html was altered or run parallel?

## History


## Credits

Johannes Gräter

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
