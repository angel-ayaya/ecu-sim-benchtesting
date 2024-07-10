import tkinter as tk
from tkinter import ttk
import can

class CANTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAN Test Interface")

        self.create_widgets()
        self.can_bus = None
        self.monitoring = False

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.message_list_frame = ttk.LabelFrame(frame, text="Message Log", padding="10")
        self.message_list_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        columns = ("Arbitration ID", "Data")
        self.message_list = ttk.Treeview(self.message_list_frame, columns=columns, show='headings')
        self.message_list.heading("Arbitration ID", text="Arbitration ID")
        self.message_list.heading("Data", text="Data")
        self.message_list.column("Arbitration ID", width=120)
        self.message_list.column("Data", width=200)
        self.message_list.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(self.message_list_frame, orient=tk.VERTICAL, command=self.message_list.yview)
        self.message_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))

        self.start_button = ttk.Button(frame, text="Start Listening", command=self.start_listening)
        self.start_button.grid(column=0, row=1, padx=5, pady=5)

        self.stop_button = ttk.Button(frame, text="Stop Listening", command=self.stop_listening)
        self.stop_button.grid(column=1, row=1, padx=5, pady=5)
        self.stop_button.state(['disabled'])

        self.status_label = ttk.Label(frame, text="Status: Not Monitoring")
        self.status_label.grid(column=0, row=2, columnspan=2, pady=5)

    def start_listening(self):
        print("Starting listening...")  # Debugging statement
        try:
           
            self.can_bus = can.interface.Bus(channel='vcan0', interface='socketcan')
            print("CAN bus started successfully.")
        except Exception as e:
            print(f"Failed to start CAN bus: {e}")
            return
        self.monitoring = True

        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        self.status_label.config(text="Status: Monitoring")

        self.root.after(100, self.listen_to_can)

    def stop_listening(self):
        print("Stopping listening...")  # Debugging statement
        self.monitoring = False

        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])
        self.status_label.config(text="Status: Not Monitoring")

    def listen_to_can(self):
        if self.monitoring:
            try:
                print("Listening to CAN bus...")  # Debugging statement
                print("CanBus: ", self.can_bus)
                msg = self.can_bus.recv(1.0)  # Timeout of 1 second
                if msg:
                    print(f"Received message: {msg}")  # Debugging statement
                    self.display_message(msg)
            except can.CanError as e:
                print(f"CAN Error: {e}")
            except Exception as e:
                print(f"Error receiving CAN message: {e}")
            finally:
                self.root.after(100, self.listen_to_can)

    def display_message(self, msg):
        print(f"Displaying message: {msg}")  # Debugging statement
        self.message_list.insert('', tk.END, values=(hex(msg.arbitration_id), list(msg.data)))

def main():
    root = tk.Tk()
    app = CANTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
