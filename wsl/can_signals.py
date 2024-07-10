import can
import threading
import time

class CANSignalSimulator:
    def __init__(self, bus):
        self.bus = bus
        self.signals = [
            # Motor
            {'id': 0x100, 'data': [0x00, 0xFA], 'interval': 0.1},  # RPM del Motor
            {'id': 0x101, 'data': [0x5A], 'interval': 1},         # Temperatura del Motor
            {'id': 0x102, 'data': [0x7F], 'interval': 0.1},       # Estado del Acelerador
            {'id': 0x103, 'data': [0x2A], 'interval': 1},         # Presión del Aceite
            # Transmisión
            {'id': 0x200, 'data': [0x03], 'interval': 1},         # Estado de la Transmisión
            {'id': 0x201, 'data': [0x4B], 'interval': 1},         # Temperatura del Fluido de la Transmisión
            # Frenos
            {'id': 0x300, 'data': [0x01], 'interval': 1},         # Estado del ABS
            {'id': 0x301, 'data': [0x2A], 'interval': 1},         # Presión de los Frenos
            {'id': 0x302, 'data': [0x00], 'interval': 1},         # Estado del Freno de Mano
            # Dirección
            {'id': 0x400, 'data': [0x15], 'interval': 0.1},       # Ángulo de Dirección
            {'id': 0x401, 'data': [0x1E], 'interval': 0.1},       # Asistencia de la Dirección
            # Luces
            {'id': 0x500, 'data': [0x01], 'interval': 1},         # Estado de los Faros
            {'id': 0x501, 'data': [0x02], 'interval': 1},         # Indicadores de Giro
            # Climatización
            {'id': 0x600, 'data': [0x1E], 'interval': 1},         # Temperatura del Aire
            {'id': 0x601, 'data': [0x01], 'interval': 1},         # Estado del Compresor de AC
            # Entretenimiento
            {'id': 0x700, 'data': [0x03], 'interval': 1},         # Información de Audio
            {'id': 0x701, 'data': [0x12, 0x34], 'interval': 1},   # Datos de Navegación
            # Seguridad
            {'id': 0x800, 'data': [0x00], 'interval': 1},         # Estado de las Puertas
            {'id': 0x801, 'data': [0x01], 'interval': 1},         # Estado de los Cinturones
            {'id': 0x802, 'data': [0x01], 'interval': 1},         # Estado de los Airbags
        ]
        self.threads = []
        self.running = False

    def start(self):
        self.running = True
        for signal in self.signals:
            thread = threading.Thread(target=self.send_signal, args=(signal,))
            thread.start()
            self.threads.append(thread)

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()

    def send_signal(self, signal):
        while self.running:
            msg = can.Message(arbitration_id=signal['id'], data=signal['data'], is_extended_id=False)
            self.bus.send(msg)
            time.sleep(signal['interval'])

