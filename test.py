import asyncio
from bleak import BleakScanner

async def main():
    stop_event = asyncio.Event()

    # TODO: add something that calls stop_event.set()

    def callback(device, advertising_data):
        # TODO: do something with incoming data
        print(device.rssi)
        print(device.name)
        print(device.metadata)
        print(device.address)
        print(device.details)

    await BleakScanner.discover()

    # scanner stops when block exits
    ...

devices = await BleakScanner.discover()
print(devices)
