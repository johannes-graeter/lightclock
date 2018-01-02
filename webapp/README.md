# Lightclock Webapp

This webapp enables configuring settings and wakeup time of the lightclock.

## Installation

### 1. Dependencies

Install *picoweb* and its dependencies *utemplate* and *micropython-pkg_resources* using upip on the board:

    import upip
    upip.install("picoweb")
    upip.install("utemplate")
    upip.install("micropython-pkg_resources")

*Note: picoweb fails trying to install its dependencies (at least on my ESP8266), thats why we install them manually. picoweb itself should be installed successfully.*

Now, you should have a lib file tree like this:

    /lib
    ├── picoweb
    │   └── __init__.py
    │   └── utils.py
    ├── utemplate
    │   └── compiled.py
    │   └── source.py
    └── pkg_resources.py

### 2. Compile templates

As online template rendering using `utemplate.source` is too memory expensive for our purpose, we compile the HTML template to a python rendering script offline.

1. Clone utemplate:  
    `git clone https://github.com/pfalcon/utemplate.git <path_to_utemplate>`

2. Compile config.html to config_html.py:  
    `python3 <path_to_utemplate>/utemplate_util.py "rawcompile" webapp/templates/config.html`

### 3. Minimize file size

We gzip `bootstrap.min.css` such that the Webapp can provide the compressed version and reduce loading time from 6-8s to 1.6-1.7s:

    gzip -c --best webapp/bootstrap.min.css > webapp/bootstrap.min.css.gz

We can also strip trailing whitespace and linebreaks from the dynamic HTML page reducing file size by ~40%

    sed -e "s/^[[:space:]]*//g" webapp/templates/config.html | tr -d '\n' > webapp/templates/config.html.min
    python3 <path_to_utemplate>/utemplate_util.py "rawcompile" webapp/templates/config.html.min
    mv webapp/templates/config_html_min.py webapp/templates/config_html.py

### 4. Copy Webapp files to board

Copy the webapp files (including the compiled template and compressed stylesheet) to your MicroPython board into the webapp folder, eg.:

    ampy put webapp

## Testing

1. Use the `main_webapp_test.py` for testing. It also needs `connect_to_router.py`, `config_wifi.json` and `config.json`.

    `ampy put main_webapp_test.py main.py`
2. Reboot (prefer hard-reboot as MicroPython does not properly close sockets on soft-reboot, causing the webapp to crash after soft-reboot)
3. Connect to the same network as the board
4. Open `http://<static_ip>:8081/` in a browser
5. Enjoy the webapp
