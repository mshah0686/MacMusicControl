# DataCapture
# Created at 2020-05-28 20:04:20.039317
import streams
from nxp.hexiwear import hexiwear


streams.serial() 
hexi = hexiwear.HEXIWEAR()
while True:
    acc = hexi.get_accelerometer_data()
    print(str(acc[0]) + ',' + str(acc[1]) + ',' + str(acc[2]))
    sleep(10)