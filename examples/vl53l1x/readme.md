# VL53L1X guideline

## Install Library
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
cd ~
sudo pip3 install --upgrade vl53l1x
```

https://github.com/pimoroni/vl53l1x-python

## Using the second I2C port on Raspberry Pi
```
sudo vi /boot/config.txt
```
Add `dtparam=i2c_vc=on`

To check the peripherals are properly connected, run
`sudo i2cdetect -y 1` and `sudo i2cdetect -y 0`

## Changing default address of a vl53l1x sensor
The default I2C bus address of a vl53l1x sensor is 0x29.
To handle two I2C bus port, the address should be adjusted.
Chainging address is included in the code.

https://github.com/pimoroni/vl53l1x-python/blob/master/examples/change-address.py

run
```
sudo i2cdetect -y 0
sudo i2cdetect -y 1
```
to check the address of the sensor.

## Other References

pin connection  
https://linuxhint.com/gpio-pinout-raspberry-pi/  
https://learn.adafruit.com/adafruit-vl53l1x/python-circuitpython
