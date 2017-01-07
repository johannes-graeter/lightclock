# Lightclock

Code for realizing a fading light clock on a micropython capable board.
Tested with HUZZAH ESP8266 Feather.

## Installation

* Install micropython on board <https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html>
* Copy main.py
* branch off an on, main will start on boot

## Usage

Offline:
* plugin your usb cabel and modify config.json and alarmtime.json   

Online:
* set up static IP on your router

EITHER: 
* Send file using WebRepl <http://micropython.org/webrepl/>

OR:
* access the html interface to modfiy the configs (not yet implemented)

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
