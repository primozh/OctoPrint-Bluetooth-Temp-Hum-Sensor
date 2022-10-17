import asyncio
import threading
from bleak import BleakScanner

from octoprint_bluetooth_temp_hum_sensor.bt_parser import BTParser

class BluetoothAdvertismentAnalyzer:

    def __init__(self, identifier, mac_address, aeskeys, logger, plugin_manager):
        self.identifier = identifier
        self.mac_address = mac_address
        self.aeskeys = aeskeys
        self.logger = logger
        self.bleparser = BTParser(logger, self.aeskeys)
        self.plugin_manager = plugin_manager

        self.thread = threading.Thread(target=self.start, daemon=True)
        self.thread.start()

    def start(self):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.run())
    
    def stop(self):
        self.logger.info("Scanning stopped")
        self.stop_event.clear()

    async def run(self):
        self.stop_event = asyncio.Event()
        self.stop_event.set()

        data = dict(
                    temperature= "- °C",
                    humidity="- %",
                    battery="- %"
                )
        self.logger.debug("Sending data %s, %s", self.identifier, data)
        self.plugin_manager.send_plugin_message(self.identifier, data)

        self.logger.info("Started scanning for BT devices")
        async with BleakScanner(self.callback) as scanner:
            await self.stop_event.wait()
        
    def callback(self, device, advertising_data):
        # self.logger.info("Found %s", device)

        if device.address == self.mac_address:
            result = self.bleparser.parse_data(device.address, advertising_data)

            if "temperature" in result:
                data = dict(
                    temperature= "{:.2f} °C".format(result["temperature"]),
                    humidity="{:.2f} %".format(result["humidity"]),
                    battery="{} %".format(result["battery"])
                )
                self.logger.debug("Sending data %s, %s", self.identifier, data)
                self.plugin_manager.send_plugin_message(self.identifier, data)
            else:
                self.logger.debug("No data in packet!")

