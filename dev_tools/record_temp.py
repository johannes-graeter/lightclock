# 5 : D1 : SDL
# 4 : D2 : SDA
from machine import Pin, I2C
import mcp9808
import utime

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
mcp = mcp9808.MCP9808(i2c=i2c)
mcp.set_resolution(mcp9808.T_RES_MAX)

logfile = open("temp_log.csv", "a")
logfile.write("\n\n\ntime,temp\n")

try:
    while True:
        # temp = mcp.get_temp()
        temp, frac = mcp.get_temp_int()
        print ("Temperature is: {:d}.{:d}".format(temp, frac))
        logfile.write("{:d},{:d}.{:d}\n".format(utime.time(), temp, frac))
        utime.sleep(9)
except KeyboardInterrupt:
    print("ctrl+c pressed, quitting")
    logfile.close()
