def do_connect(configName, timeout):
    import network
    import ujson as json
    import machine
    import time
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        print('reading config ' + configName)

        try:
            config = json.load(open(configName, "r"))
        except:
            print("couldn't read " + configName)
            return False

        if not ("ssid" in config and "password" in config):
            return False

        print("ssid=" + config["ssid"])
        sta_if.active(True)
        sta_if.connect(config["ssid"], config["password"])

        start_time = time.ticks_ms()
        while not sta_if.isconnected():
            # print dashes every 0.1 seconds
            print("-", end="")
            machine.idle()

            if time.ticks_diff(time.ticks_ms(), start_time) > timeout:
                print("connecting timed out, stop reconnecting")
                sta_if.active(False)
                return False

        # TODO get rid of static IP, provide the current IP via webapp
        # assign static ip from config
        if "static_ip" in config:
            lst_current_config = list(sta_if.ifconfig())
            lst_current_config[0] = config["static_ip"]
            sta_if.ifconfig(tuple(lst_current_config))

    # TODO assign static ip if already connected, but different from config?

    print('network config:', sta_if.ifconfig())
    return True
