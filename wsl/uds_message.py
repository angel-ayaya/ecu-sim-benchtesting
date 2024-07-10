import can

class UDSMessage:
    def __init__(self, arbitration_id, service_id, data):
        self.arbitration_id = arbitration_id
        self.service_id = service_id
        self.data = data

    def encode(self):
        return can.Message(arbitration_id=self.arbitration_id, data=bytes([self.service_id]) + self.data, is_extended_id=False)

    @classmethod
    def decode(cls, msg):
        arbitration_id = msg.arbitration_id
        service_id = msg.data[0]
        data = msg.data[1:]
        return cls(arbitration_id, service_id, data)

    def __repr__(self):
        return f"UDSMessage(arbitration_id={hex(self.arbitration_id)}, service_id={hex(self.service_id)}, data={self.data})"
