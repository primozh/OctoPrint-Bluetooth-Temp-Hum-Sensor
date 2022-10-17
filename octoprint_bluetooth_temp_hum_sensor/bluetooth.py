import asyncio
import imp
import logging
import random
import threading
from bleak import BleakScanner

from octoprint_bluetooth_temp_hum_sensor.ble_parser.bt_parser import BTParser

class BluetoothAdvertismentAnalyzer:

    def __init__(self, identifier, mac_address, aeskeys, logger, plugin_manager):
        self.identifier = identifier
        self.mac_address = mac_address
        self.aeskeys = aeskeys
        self.logger = logger
        self.bleparser = BTParser(logger, self.aeskeys)
        self.plugin_manager = plugin_manager

        self._scanner = None
        self.thread = threading.Thread(target=self.start, daemon=True)
        self.thread.start()


    def start(self):
        self.logger.info("Starting new Thread")
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.run())

    async def run(self):
        self.logger.info("Started scanning for BT devices")
        async with BleakScanner(self.callback) as scanner:
            pass
        
    def callback(self, device, advertising_data):
        # self.logger.info("Found %s", device)

        if device.address == self.mac_address:
            result = self.bleparser.parse_data(device.address, advertising_data)
            self.logger.info("%s", result["temperature"])

            if "temperature" in result:
                data = dict(
                    Temperature= "{:.2f}".format(result["temperature"]),
                    Humidity="{:.2f}".format(result["humidity"]),
                    Battery=result["battery"]
                )
                self.logger.info("Sending data! %s, %s", self.identifier, data)
                self.plugin_manager.send_plugin_message(self.identifier, data)
            else:
                self.logger.info("No data in packet!")

