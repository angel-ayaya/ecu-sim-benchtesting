import can

def receive_can_messages():
    # Crear un bus CAN en la interfaz virtual vcan0
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    print("Esperando mensajes CAN...")

    while True:
        # Recibir un mensaje del bus CAN
        msg = bus.recv()

        if msg:
            print(f"Mensaje recibido: {msg}")

if __name__ == "__main__":
    receive_can_messages()
