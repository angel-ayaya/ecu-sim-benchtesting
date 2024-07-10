import can
from uds_message import UDSMessage  # Importar UDSMessage

class CANBus:
    def __init__(self, channel='vcan0', interface='socketcan'):
        self.bus = can.interface.Bus(channel=channel, bustype=interface)

    def send(self, msg):
        # Envía un mensaje UDS por el bus CAN
        self.bus.send(msg.encode())
        print(f"Mensaje enviado: {msg}")

    def recv(self):
        # Recibe un mensaje UDS del bus CAN
        msg = self.bus.recv(timeout=1)
        if msg:
            return UDSMessage.decode(msg)
        return None

    def shutdown(self):
        # Método placeholder, no es necesario shutdown en socketcan
        pass
