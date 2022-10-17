# OctoPrint Bluetooth Temperature and Humidity sensor plugin

Listens for Bluetooth advertisement messages that contains temperature, humidity and battery information for nearby device with user configured MAC address.

Can be used with any device capable of producing BTHome formatted messages: https://bthome.io/

**Only non-encrypted messages are supported as of now**

## Setup

Install manually using this URL:

    https://github.com/primozh/OctoPrint-Bluetooth-Temp-Hum-Sensor/archive/master.zip

And set up MAC address on Plugin Settings page.

## Configuration

* MAC address: device that is sending the data
* Show temperature: ON/OFF
* Show humidity: ON/OFF
* Show battery: ON/OFF