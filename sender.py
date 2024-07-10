import can
import time

def send_can_messages():
    # Crear un bus CAN en la interfaz virtual vcan0
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    while True:
        # Crear un mensaje CAN
        msg = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33, 0x44], is_extended_id=False)
        
        try:
            # Enviar el mensaje en el bus CAN
            bus.send(msg)
            print(f"Mensaje enviado: {msg}")
        except can.CanError:
            print("Error al enviar el mensaje")

        # Esperar 1 segundo antes de enviar el siguiente mensaje
        time.sleep(1)

if __name__ == "__main__":
    send_can_messages()
