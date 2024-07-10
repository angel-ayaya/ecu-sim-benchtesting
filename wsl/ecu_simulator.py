from uds_message import UDSMessage

class ECUSimulator:
    def __init__(self):
        self.dids = {}
        self.dtcs = {}

    def process_message(self, msg):
        if msg.service_id == 0x22:  # Read Data by Identifier
            return self.handle_read_did(msg)
        elif msg.service_id == 0x2E:  # Write Data by Identifier
            return self.handle_write_did(msg)
        else:
            return None

    def handle_read_did(self, msg):
        did = int.from_bytes(msg.data[:2], 'big')
        if did in self.dids:
            value = self.dids[did]
            response = UDSMessage(arbitration_id=0x7E8, service_id=0x62, data=did.to_bytes(2, 'big') + value.to_bytes(2, 'big'))
            return response
        return None

    def handle_write_did(self, msg):
        did = int.from_bytes(msg.data[:2], 'big')
        value = int.from_bytes(msg.data[2:], 'big')
        if did in self.dids:
            self.dids[did] = value
            response = UDSMessage(arbitration_id=0x7E8, service_id=0x6E, data=did.to_bytes(2, 'big') + value.to_bytes(2, 'big'))
            return response
        return None
