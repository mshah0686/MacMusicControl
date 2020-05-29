# DataCapture
# Created at 2020-05-28 20:04:20.039317
import streams
from nxp.hexiwear import hexiwear


streams.serial() 
hexi = hexiwear.HEXIWEAR()

hexi.draw_text("Start!", 0, 60, 96, 20, align=3, color=0xFFFF, background=0x0000, encode=False)

while True:
    acc = hexi.get_accelerometer_data()
    print(str(acc[0]) + ',' + str(acc[1]) + ',' + str(acc[2]))
    #milliseconds: 1000 = 1 second
    #1 second * 1/100 per second * 1000 conversion = 10 => 100 hertz
    sleep(10)