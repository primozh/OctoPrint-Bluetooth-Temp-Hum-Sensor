import asyncio
import threading
from bleak import BleakScanner

class BluetoothScanner:

    def __init__(self, identifier, logger, plugin_manager):
        self.identifier = identifier
        self.logger = logger
        self.plugin_manager = plugin_manager
        self.detected_devices = dict()

        self.thread = threading.Thread(target=self.start, daemon=True)
        self.thread.start()

    def start(self):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.run())
    
    def stop(self):
        self.logger.info("Scanning stopped")
        self.stop_event.set()

    async def run(self):
        self.stop_event = asyncio.Event()
        self.logger.info("Started scanning for BT devices")
        async with BleakScanner(self.callback) as scanner:
            await self.stop_event.wait()
        
    def callback(self, device, advertising_data):        
        if device.address not in self.detected_devices:
            self.logger.info("%s", device.name)
            self.detected_devices[device.address] = device.name
            self.logger.info("%s", self.detected_devices)

            data = dict(device= dict(name = device.name, mac = device.address))
            self.plugin_manager.send_plugin_message(self.identifier, data)

