# rfm69-python

## Overview

This is a Python port of [Felix Rusu's RFM69 library](https://github.com/LowPowerLab/RFM69) for Arduino microcontrollers.

You will need a Beaglebone Black running a 3.8.x Linux kernel. Testing and development has been done using [Debian](>http://elinux.org/BeagleBoardDebian).

You'll need to install the [Adafruit BBIO library](https://github.com/adafruit/adafruit-beaglebone-io-python) as well.

##Status

The included moteino_gateway.py example is able to receive packets from a Moteino Node, but transmission/acks are still being worked on.

##Notes
The hardware SPI module is used. The pinout is P9_18 = MOSI, P9_21 = MISO, P9_22 = SCK. Two other GPIOs are needed, one for the chip select (P9_12), and one for an interrupt from the RFM69 (P9_13). These can be adjusted in rfm69.py if desired. The chip select is just a regular GPIO, because I had difficulty with the chip select under the Adafruit GPIO.

A pullup to 3.3V on the chip select is recommended, without it, the BBB will hang when it boots, probably due to a conflict with the SD card or something (I haven't checked the schematic to see what else is sharing that bus).