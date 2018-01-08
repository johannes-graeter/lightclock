import gc

gc.collect()
print(gc.mem_free())

import connect_to_router
connect_to_router.do_connect("config_wifi.json")

gc.collect()
print(gc.mem_free())

import webapp
app = webapp.WebApp(host="192.168.0.27")

gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())