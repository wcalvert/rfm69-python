# rfm69-python

## Overview
This is a Python port of [Felix Rusu's RFM69 library](https://github.com/LowPowerLab/RFM69) which is a part of his Moteino project.

You will need a Beaglebone Black running a 3.8.x Linux kernel. Testing and development has been done using [Debian](>http://elinux.org/BeagleBoardDebian).

You'll need to install the [Adafruit BBIO library](https://github.com/adafruit/adafruit-beaglebone-io-python) as well.

##Status
Transmission, reception, acks, retries, encryption have been tested and seem to be working well.

##How-To
Wire up the RFM69 module first. Then clone the repository, change to the directory, and try running the included examples as root:

```
git clone https://github.com/wcalvert/rfm69-python
cd rfm69-python
su
python moteino_gateway.py
```

##Pinout
The hardware SPI module is used. The pinout is:

```
P9_1 or P9_2 = Gnd
P9_3 or P9_4 = 3.3V
P9_18 = MOSI
P9_21 = MISO
P9_22 = SCK 
P9_12 = NSS
P9_13 = DIO0 
```

The chip select (NSS) and interrupt pin (DIO0) can be adjusted in rfm69.py if desired. They are just normal GPIO pins.

##Notes
A pullup to 3.3V on the chip select is recommended, without it, the BBB will hang when it boots, probably due to a conflict with the SD card or something (I haven't checked the schematic to see what else is sharing that bus).