import struct

def parse_uint(data_obj, factor=1):
    """convert bytes (as unsigned integer) and factor to float"""
    decimal_places = -int(f'{factor:e}'.split('e')[-1])
    return round(int.from_bytes(data_obj, "little", signed=False) * factor, decimal_places)


def parse_int(data_obj, factor=1):
    """convert bytes (as signed integer) and factor to float"""
    decimal_places = -int(f'{factor:e}'.split('e')[-1])
    return round(int.from_bytes(data_obj, "little", signed=True) * factor, decimal_places)


def parse_float(data_obj, factor=1):
    """convert bytes (as float) and factor to float"""
    decimal_places = -int(f'{factor:e}'.split('e')[-1])
    if len(data_obj) == 2:
        [val] = struct.unpack('e', data_obj)
    elif len(data_obj) == 4:
        [val] = struct.unpack('f', data_obj)
    elif len(data_obj) == 8:
        [val] = struct.unpack('d', data_obj)
    else:
        return None
    return round(val * factor, decimal_places)


def parse_string(data_obj, factor=None):
    """convert bytes to string"""
    return data_obj.decode('UTF-8')


def parse_mac(data_obj):
    """convert bytes to mac"""
    if len(data_obj) == 6:
        return data_obj[::-1]
    else:
        return None


dispatch = {
    0x00: parse_uint,
    0x01: parse_int,
    0x02: parse_float,
    0x03: parse_string,
    0x04: parse_mac,
}

DATA_MEAS_DICT = {
    0x00: ["packet", 1, ""],
    0x01: ["battery", 1, "%"],
    0x02: ["temperature", 0.01, "°C"],
    0x03: ["humidity", 0.01, "%"]
}

class BTHome:

    def parse_bthome(self, uuid16, source_mac, data, aeskeys):
        ha_ble_mac = source_mac
        result = {}
        packet_id = None

        if uuid16 == 0x181C:
            # Non-encrypted BTHome format
            payload = data
            packet_id = None
        else:
            return None

        if not payload:
            return None

        payload_length = len(payload)
        payload_start = 0
        
        while payload_length >= payload_start + 1:
            obj_control_byte = payload[payload_start]
            obj_data_length = (obj_control_byte >> 0) & 31  # 5 bits (0-4)
            obj_data_format = (obj_control_byte >> 5) & 7  # 3 bits (5-7)
            obj_meas_type = payload[payload_start + 1]
            next_start = payload_start + 1 + obj_data_length

            if obj_data_length != 0:
                if obj_data_format <= 3:
                    if obj_meas_type in DATA_MEAS_DICT:
                        meas_data = payload[payload_start + 2:next_start]
                        meas_type = DATA_MEAS_DICT[obj_meas_type][0]
                        meas_factor = DATA_MEAS_DICT[obj_meas_type][1]
                        meas = dispatch[obj_data_format](meas_data, meas_factor)
                        result.update({meas_type: meas})


            payload_start = next_start

        # Check for duplicate messages
        if packet_id:
            try:
                prev_packet = self.lpacket_ids[ha_ble_mac]
            except KeyError:
                # start with empty first packet
                prev_packet = None
            if prev_packet == packet_id:
                # only process new messages
                if self.filter_duplicates is True:
                    return None
            self.lpacket_ids[ha_ble_mac] = packet_id
        else:
            packet_id = "no packet id"

        return result
