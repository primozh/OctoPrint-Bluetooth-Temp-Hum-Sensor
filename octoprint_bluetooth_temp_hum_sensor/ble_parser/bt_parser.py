

import uuid

from octoprint_bluetooth_temp_hum_sensor.ble_parser.bt_home import parse_bthome


class BTParser:

    def __init__(self, logger, aeskeys=None):
        self.logger = logger
        self.aeskeys = aeskeys

    def parse_data(self, mac_address, advertising_data):
        for key in advertising_data.service_data:
            self.logger.info("%s", key)
            service_data = advertising_data.service_data[key]

            # parse data for sensors with service data
            bytekey = uuid.UUID(key).bytes
            uuid16 = int.from_bytes(bytekey[2:4], "big")

            if uuid16 in [0x181C, 0x181E]:
                self.logger.info("BTHome format. Parsing...")
                return parse_bthome(uuid16, mac_address, service_data, self.aeskeys)