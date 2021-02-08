from display1602 import LCD
import utime

def get_temperature(nrMeasurements):
    sum = 0
    for i in range(nrMeasurements):
        sum += machine.ADC(4).read_u16()
    sensor_temp = (1.0*sum) / nrMeasurements # average to improve accuracy
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

lcd = LCD()
lcd.clear()
lcd.write_line1( 'Temperature:', 1 )
lcd.write_line2( "{0:2.1f}".format(get_temperature(10)), 1 )
utime.sleep(4)
lcd.clear()

