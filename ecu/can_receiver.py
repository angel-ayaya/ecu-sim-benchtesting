import can

class CANReceiver:
    def __init__(self, channel='test', interface='virtual'):
        self.bus = can.interface.Bus(channel=channel, interface=interface)
        self.msg = None

    def receive_once(self):
        print("Esperando mensaje...")
        self.msg = self.bus.recv(timeout=1)
        if self.msg:
            print(f"Mensaje recibido: {self.msg}")
        else:
            print("No se recibió ningún mensaje en el último segundo.")
        return self.msg

    def shutdown(self):
        self.bus.shutdown()
