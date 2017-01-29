def do_connect(configName):
    import network
    import ujson as json
    import machine
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        print('reading config '+configName)
        config = {}

        while not ("ssid" in config and "password" in config):
            try:
                config = json.load(open(configName, "r"))
            except:
                print("couldn't read "+configName)

        print("ssid="+config["ssid"])
        sta_if.active(True)
        sta_if.connect(config["ssid"], config["password"])

        while not sta_if.isconnected():
            # print dashes every 0.1 seconds
            print("-", end="")
            machine.idle()

    # assign static ip from config
    if "static_ip" in config:
        lst_current_config = list(sta_if.ifconfig())
        lst_current_config[0] = config["static_ip"]
        sta_if.ifconfig(tuple(lst_current_config))

    print('network config:', sta_if.ifconfig())
