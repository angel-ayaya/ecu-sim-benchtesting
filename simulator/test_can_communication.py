import pytest
import threading
import time
import can_simulator
import can_receiver

bus_config = {
    'channel': 'test',
    'interface': 'virtual',
    'arbitration_id': 0xabcde,
    'data': bytearray([1, 2, 3])
}

def test_can_communication():
    stop_event = threading.Event()
    
    simulator = can_simulator.ECUSimulator(bus_config)
    receiver = can_receiver.CANReceiver(bus_config)
    
    def run_simulator(simulator):
        while not stop_event.is_set():
            simulator.run_once()
            time.sleep(1)
    
    def run_receiver(receiver):
        while not stop_event.is_set():
            receiver.run_once()
            time.sleep(1)
    
    simulator_thread = threading.Thread(target=run_simulator, args=(simulator,))
    receiver_thread = threading.Thread(target=run_receiver, args=(receiver,))
    
    simulator_thread.start()
    receiver_thread.start()
    
    time.sleep(5)  # Espera a que se envíen y reciban algunos mensajes
    
    stop_event.set()
    
    simulator_thread.join()
    receiver_thread.join()
    
    # Aquí puedes agregar validaciones específicas
    assert True  # Reemplaza con validaciones reales

if __name__ == "__main__":
    pytest.main()
