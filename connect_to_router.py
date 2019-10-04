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
            sta_if.active(False)
            return False

        if not ("wifi_ssid" in config and config["wifi_ssid"]["value"]
                and "wifi_password" in config and "value" in config["wifi_password"]):
            sta_if.active(False)
            return False

        print("ssid=" + config["wifi_ssid"]["value"])
        sta_if.active(True)
        sta_if.connect(config["wifi_ssid"]["value"], config["wifi_password"]["value"])

        start_time = time.ticks_ms()
        while not sta_if.isconnected():
            # print dashes every 0.1 seconds
            print("-", end="")
            machine.idle()

            if time.ticks_diff(time.ticks_ms(), start_time) > timeout:
                print("-")
                print("connecting timed out, stop reconnecting")
                sta_if.active(False)
                return False

        # TODO get rid of static IP or provide proper error handling (what if IP differs from static_ip after connecting? reconnecting might not help as the IP might be unavailable)
        # assign static ip from config
        if "wifi_static_ip" in config:
            lst_current_config = list(sta_if.ifconfig())
            lst_current_config[0] = config["wifi_static_ip"]["value"]
            sta_if.ifconfig(tuple(lst_current_config))

    print('network config:', sta_if.ifconfig())
    return True
