import gc

gc.collect()
print(gc.mem_free())

import connect_to_router
connect_to_router.do_connect("config_wifi.json")

gc.collect()
print(gc.mem_free())

import webapp