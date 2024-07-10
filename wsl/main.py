import tkinter as tk
from tkinter import ttk
import can
import time
import threading
import queue

class CANSignalSimulator:
    def __init__(self, bus, message_queue, start_time):
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
        self.running = False
        self.message_queue = message_queue
        self.last_sent_times = {signal['id']: 0 for signal in self.signals}
        self.start_time = start_time

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def send_signals(self):
        current_time = time.time()
        for signal in self.signals:
            if self.running and current_time - self.last_sent_times[signal['id']] >= signal['interval']:
                msg = can.Message(arbitration_id=signal['id'], data=signal['data'], is_extended_id=False)
                self.bus.send(msg)
                self.message_queue.put(msg)  # Duplicate the message internally
                print(f"Sending message: {msg}")  # Debugging statement
                self.last_sent_times[signal['id']] = current_time

class CANMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAN Monitor")

        self.create_widgets()
        self.can_bus = None
        self.simulator = None
        self.monitoring = False
        self.message_queue = queue.Queue()
        self.start_time = None

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.message_list_frame = ttk.LabelFrame(frame, text="Message Log", padding="10")
        self.message_list_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        columns = ("Time", "ID", "Name", "Event Type", "Dir", "DLC", "Data")
        self.message_list = ttk.Treeview(self.message_list_frame, columns=columns, show='headings')
        self.message_list.heading("Time", text="Time")
        self.message_list.heading("ID", text="ID")
        self.message_list.heading("Name", text="Name")
        self.message_list.heading("Event Type", text="Event Type")
        self.message_list.heading("Dir", text="Dir")
        self.message_list.heading("DLC", text="DLC")
        self.message_list.heading("Data", text="Data")

        self.message_list.column("Time", width=100)
        self.message_list.column("ID", width=60)
        self.message_list.column("Name", width=100)
        self.message_list.column("Event Type", width=100)
        self.message_list.column("Dir", width=50)
        self.message_list.column("DLC", width=50)
        self.message_list.column("Data", width=200)
        self.message_list.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(self.message_list_frame, orient=tk.VERTICAL, command=self.message_list.yview)
        self.message_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))

        self.control_frame = ttk.LabelFrame(frame, text="Controls", padding="10")
        self.control_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.start_button = ttk.Button(self.control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(column=0, row=0, padx=5, pady=5)

        self.stop_button = ttk.Button(self.control_frame, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.grid(column=1, row=0, padx=5, pady=5)
        self.stop_button.state(['disabled'])

        self.status_label = ttk.Label(self.control_frame, text="Status: Not Monitoring")
        self.status_label.grid(column=0, row=1, columnspan=2, pady=5)

    def start_simulation(self):
        print("Starting simulation...")  # Debugging statement
        try:
            self.can_bus = can.ThreadSafeBus(channel='vcan0', interface='socketcan')
            print("CAN bus started successfully.")
        except Exception as e:
            print(f"Failed to start CAN bus: {e}")
            return

        self.start_time = time.time()
        self.simulator = CANSignalSimulator(self.can_bus, self.message_queue, self.start_time)
        self.monitoring = True

        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        self.status_label.config(text="Status: Monitoring")

        self.simulator.start()
        self.root.after(100, self.update_simulation)

    def stop_simulation(self):
        print("Stopping simulation...")  # Debugging statement
        self.monitoring = False
        self.simulator.stop()

        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])
        self.status_label.config(text="Status: Not Monitoring")

    def update_simulation(self):
        if self.monitoring:
            self.simulator.send_signals()
            self.listen_to_can()
            self.root.after(100, self.update_simulation)

    def listen_to_can(self):
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                print(f"Received message: {msg}")  # Debugging statement
                self.display_message(msg)
        except can.CanError as e:
            print(f"CAN Error: {e}")
        except Exception as e:
            print(f"Error receiving CAN message: {e}")

    def display_message(self, msg):
        timestamp = time.time() - self.start_time
        arbitration_id = hex(msg.arbitration_id)
        data = ' '.join(format(x, '02x') for x in msg.data)
        dlc = msg.dlc
        event_type = "CAN Frame"
        direction = "Tx" if msg.is_rx is False else "Rx"
        name = self.get_message_name(msg.arbitration_id)

        print(f"Displaying message: {msg}")  # Debugging statement
        self.message_list.insert('', 0, values=(timestamp, arbitration_id, name, event_type, direction, dlc, data))

    def get_message_name(self, arbitration_id):
        # Implement a mapping from arbitration ID to message name if required
        # For now, we'll just return a placeholder
        return "Message_Name"

def main():
    root = tk.Tk()
    app = CANMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
