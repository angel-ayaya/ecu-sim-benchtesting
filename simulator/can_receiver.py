import can

class CANReceiver:
    def __init__(self, bus_config):
        self.bus = can.interface.Bus(channel=bus_config['channel'], interface=bus_config['interface'])
        self.msg = None

    def run_once(self):
        print("Esperando mensaje...")
        self.msg = self.bus.recv(timeout=1)
        if self.msg:
            print(f"Mensaje recibido: {self.msg}")
            if self.msg.data in [bytearray([1, 2, 3]), bytearray([4, 5, 6])]:
                print("Mensaje validado correctamente")
            else:
                print(f"Datos inesperados: {self.msg.data}")
        else:
            print("No se recibió ningún mensaje en el último segundo.")
    
    def shutdown(self):
        self.bus.shutdown()
