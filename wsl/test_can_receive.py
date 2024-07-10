import can

def main():
    try:
        can_bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
        print("CAN bus started successfully.")
        
        while True:
            msg = can_bus.recv(1.0)  # Timeout of 1 second
            if msg:
                print(f"Received message: {msg}")

    except Exception as e:
        print(f"Failed to start CAN bus: {e}")

if __name__ == "__main__":
    main()
