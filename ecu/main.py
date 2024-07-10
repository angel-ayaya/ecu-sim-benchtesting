import threading
import time
import tkinter as tk
from tkinter import ttk
import can_receiver

receiver = can_receiver.CANReceiver()

stop_event = threading.Event()

def run_receiver(receiver, message_list):
    while not stop_event.is_set():
        msg = receiver.receive_once()
        if msg:
            message_list.insert('', tk.END, values=(f"{hex(msg.arbitration_id)}", f"{list(msg.data)}"))
        time.sleep(0.1)

def create_ui():
    root = tk.Tk()
    root.title("CAN Monitor")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    message_list_frame = ttk.LabelFrame(frame, text="Message Log", padding="10")
    message_list_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    columns = ("Arbitration ID", "Data")
    message_list = ttk.Treeview(message_list_frame, columns=columns, show='headings')
    message_list.heading("Arbitration ID", text="Arbitration ID")
    message_list.heading("Data", text="Data")
    message_list.column("Arbitration ID", width=120)
    message_list.column("Data", width=200)
    message_list.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scrollbar = ttk.Scrollbar(message_list_frame, orient=tk.VERTICAL, command=message_list.yview)
    message_list.configure(yscroll=scrollbar.set)
    scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))

    # Iniciar el hilo del receptor después de crear la UI
    receiver_thread = threading.Thread(target=run_receiver, args=(receiver, message_list))
    receiver_thread.start()

    def on_close():
        stop_event.set()
        receiver_thread.join()
        receiver.shutdown()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

create_ui()
