import threading
import time
import tkinter as tk
from tkinter import ttk
import can_simulator
import can_receiver
import visualizer
import can

bus_config = {
    'channel': 'test',
    'interface': 'virtual',
    'arbitration_id': 0xabcde,
    'data': bytearray([1, 2, 3])
}

simulator = can_simulator.ECUSimulator(bus_config)
receiver = can_receiver.CANReceiver(bus_config)
vis = visualizer.CANVisualizer()

stop_event = threading.Event()

sleep_time = 1

def run_simulator(simulator):
    while not stop_event.is_set():
        simulator.run_once()
        time.sleep(sleep_time)

def run_receiver(receiver, vis, message_list):
    while not stop_event.is_set():
        receiver.run_once()
        if receiver.msg:
            vis.add_data(receiver.msg.data[0])
            message_list.insert('', tk.END, values=(f"Received", f"{hex(receiver.msg.arbitration_id)}", f"{list(receiver.msg.data)}"))
        time.sleep(sleep_time)

def send_custom_message(arbitration_id, data, message_list):
    msg = can.Message(arbitration_id=int(arbitration_id, 16), data=bytearray(eval(data)))
    simulator.bus.send(msg)
    print(f"Mensaje enviado manualmente: {msg}")
    message_list.insert('', tk.END, values=(f"Sent", f"{hex(msg.arbitration_id)}", f"{list(msg.data)}"))

def create_ui():
    root = tk.Tk()
    root.title("CAN Simulator")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Arbitration ID:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    arbitration_id_entry = ttk.Entry(frame)
    arbitration_id_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    ttk.Label(frame, text="Data:").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    data_entry = ttk.Entry(frame)
    data_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    message_list_frame = ttk.LabelFrame(frame, text="Message Log", padding="10")
    message_list_frame.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    columns = ("Type", "Arbitration ID", "Data")
    message_list = ttk.Treeview(message_list_frame, columns=columns, show='headings')
    message_list.heading("Type", text="Type")
    message_list.heading("Arbitration ID", text="Arbitration ID")
    message_list.heading("Data", text="Data")
    message_list.column("Type", width=80)
    message_list.column("Arbitration ID", width=120)
    message_list.column("Data", width=200)
    message_list.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scrollbar = ttk.Scrollbar(message_list_frame, orient=tk.VERTICAL, command=message_list.yview)
    message_list.configure(yscroll=scrollbar.set)
    scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))

    def on_send_button_click():
        arbitration_id = arbitration_id_entry.get()
        data = data_entry.get()
        send_custom_message(arbitration_id, data, message_list)

    send_button = ttk.Button(frame, text="Send Message", command=on_send_button_click)
    send_button.grid(column=0, row=3, columnspan=2, pady=10)

    # Iniciar los hilos del simulador y receptor después de crear la UI
    simulator_thread = threading.Thread(target=run_simulator, args=(simulator,))
    receiver_thread = threading.Thread(target=run_receiver, args=(receiver, vis, message_list))

    simulator_thread.start()
    receiver_thread.start()

    root.mainloop()

    stop_event.set()
    simulator_thread.join()
    receiver_thread.join()

    vis.plot()
    print('Programa cerrado')

ui_thread = threading.Thread(target=create_ui)
ui_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop_event.set()

ui_thread.join()