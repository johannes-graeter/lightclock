# Lightclock

Code for realizing a fading light clock on a micropython capable board.
Tested with HUZZAH ESP8266 Feather.

## Installation

* Download the micropython firmware with our lightclock code included from the releases page.
* Follow [micropython install instructions](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html) until point 1.5, but use our firmware bin instead.
* Deploy remaining webapp content etc. (from the release) to the board:
    * install ampy: `sudo pip2 install adafruit-ampy`
    * deploy: `make deploy-release`


## Building on your own

1. Setup the firmware folder
    * clone [micropython](https://github.com/micropython/micropython) to your workspace
    * check out the `v1.9.3` tag
    * build the unix port (as explained in the [micropython README.md](https://github.com/micropython/micropython/blob/master/README.md))
    * install `picoweb`, `utemplate` and its dependencies into the `micropython/ports/esp8266/modules` folder using `upip`:
      ```
      cd micropython/ports/esp8266/modules
      <path/to>/micropython -m upip install -p . picoweb utemplate
      <path/to>/micropython -m upip install -p . micropython-collections.deque
      ```
    * clone [micropython-lib](https://github.com/micropython/micropython-lib) to your workspace
    * check out the `v1.9.3` tag
    * override lib dependencies with correct version in the `micropython/ports/esp8266/modules` folder using soft links:
      ```
      cd micropython/ports/esp8266/modules
      rm -r pkg_resources.py uasyncio
      ln -s <path/to>/micropython-lib/pkg_resources/pkg_resources.py .
      mkdir uasyncio
      ln -s <path/to>/micropython-lib/uasyncio/uasyncio/__init__.py uasyncio/
      ln -s <path/to>/micropython-lib/uasyncio.core/uasyncio/core.py uasyncio/
      ```
    * link `alarmclock` and `webapp` folders into into the `micropython/ports/esp8266/modules` folder using soft links:
      ```
      ln -s <path/to>/lightclock/webapp .
      ln -s <path/to>/lightclock/alarmclock .
      ```

2. Build the firmware with frozen lightclock modules
    ```
    cd <path/to>/micropython/ports/esp8266
    make axtls
    make
    ```
    see also [detailed instructions here](https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules)

3. Deploy the freshly built firmware:
    * as with normal micropython firmware, erase and write the flash as described in the [micropython install instructions](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html) using the freshly build firmware `build/firmware-combined.bin` 

3. Build webapp content
    * clone [utemplate](https://github.com/pfalcon/utemplate) to your workspace
    * build the webapp templates (assumes utemplate is in the same folder as lightclock):  
    `make webapp-templates`
    * compress static stylesheets and javascripts  
    `make webapp-static`

3. Deploy webapp content etc. to the board:
    * install ampy: `sudo pip2 install adafruit-ampy`
    * deploy: `make deploy-without-modules` (it takes a while!)

3. Add temperature sensor support:
    * clone [mcp9808](https://github.com/patvdleer/micropython-mcp9808) to your workspace
    * link to it in the `micropython/ports/esp8266/modules` folder using a soft link:
      ```
      cd <path/to>/micropython/ports/esp8266/modules
      ln -s <path/to>/mcp9808/mcp9808.py .
      ```

4. Finalize
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


## Usage

Connect to `http://<static_ip>:8081/` in a browser

## Credits

Johannes Gräter
Piotr Orzechowski

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
