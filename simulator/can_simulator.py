import can
import time
import random

class ECUSimulator:
    def __init__(self, bus_config):
        self.bus = can.interface.Bus(channel=bus_config['channel'], interface=bus_config['interface'])
        self.arbitration_ids = [bus_config['arbitration_id'], 0x123456]
        self.data_patterns = [bytearray([1, 2, 3]), bytearray([4, 5, 6])]

    def run_once(self):
        try:
            start_time = time.time()
            arbitration_id = random.choice(self.arbitration_ids)
            data = random.choice(self.data_patterns)
            msg = can.Message(arbitration_id=arbitration_id, data=data)
            self.bus.send(msg)
            end_time = time.time()
            print(f"Mensaje enviado: {msg} en {end_time - start_time} segundos")
        except can.CanError:
            print("Error en la comunicación CAN")
    
    def shutdown(self):
        self.bus.shutdown()
