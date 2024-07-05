import can
import time
import random

class ECUSimulator:
    def __init__(self, bus_config):
        self.bus = can.interface.Bus(channel=bus_config['channel'], interface=bus_config['interface'])
        self.dids = {
            0x0101: 50,    # Velocidad del vehículo
            0x0102: 90,    # Temperatura del motor
            0x0103: 75,    # Nivel de combustible
            0x0104: 120,   # RPM del motor
            0x0105: 30,    # Presión de aceite
            0x0106: 1,     # Estado del faro (0: apagado, 1: encendido)
            0x0107: 12.5,  # Voltaje de la batería
            0x0108: 45,    # Temperatura del aire de admisión
            0x0109: 2,     # Estado del freno (0: liberado, 1: presionado)
            0x010A: 80     # Nivel de líquido de frenos
        }
        self.dtcs = {
            0x2001: False,  # Error en el sensor de temperatura
            0x2002: False   # Error en el sensor de velocidad
        }
        self.state = "ACTIVE"  # Inicializamos en estado ACTIVE para que empiece a enviar mensajes

    def process_message(self, msg):
        print(f"Procesando mensaje: {msg}")
        service_id = msg.data[0]
        if service_id == 0x22:  # Read Data by Identifier
            did = int.from_bytes(msg.data[1:3], 'big')
            print(f"Leyendo DID: {did}")
            if did in self.dids:
                value = self.dids[did]
                response = can.Message(arbitration_id=0x7E8, data=bytearray([0x62]) + did.to_bytes(2, 'big') + int(value).to_bytes(2, 'big'))
                self.bus.send(response)
                print(f"Respuesta a lectura de DID {did}: {value}")
            else:
                print(f"DID {did} no encontrado para lectura.")
        elif service_id == 0x2E:  # Write Data by Identifier
            did = int.from_bytes(msg.data[1:3], 'big')
            value = int.from_bytes(msg.data[3:], 'big')
            print(f"Escribiendo DID: {did} con valor: {value}")
            if did in self.dids:
                self.dids[did] = value
                response = can.Message(arbitration_id=0x7E8, data=bytearray([0x6E]) + did.to_bytes(2, 'big') + value.to_bytes(2, 'big'))
                self.bus.send(response)
                print(f"Respuesta a escritura de DID {did}: {value}")
            else:
                print(f"DID {did} no encontrado para escritura.")

    def run_once(self):
        try:
            if self.state == "ACTIVE":
                arbitration_id = 0x7DF  # Enviar mensajes al ID de arbitraje común
                did = random.choice(list(self.dids.keys()))
                data = bytearray([0x22]) + did.to_bytes(2, 'big')
                msg = can.Message(arbitration_id=arbitration_id, data=data)
                self.bus.send(msg)
                print(f"Mensaje enviado: {msg}")
            time.sleep(1)
        except can.CanError:
            print("Error en la comunicación CAN")
    
    def receive_and_process(self):
        msg = self.bus.recv(timeout=1)
        if msg:
            print(f"Mensaje recibido para procesar: {msg}")
            self.process_message(msg)
        else:
            print("No se recibió ningún mensaje.")

    def shutdown(self):
        self.bus.shutdown()
