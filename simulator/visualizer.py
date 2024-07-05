import matplotlib.pyplot as plt
import time

class CANVisualizer:
    def __init__(self):
        self.timestamps = []
        self.values = []

    def add_data(self, value):
        self.timestamps.append(time.time())
        self.values.append(value)

    def plot(self):
        plt.plot(self.timestamps, self.values)
        plt.xlabel('Tiempo')
        plt.ylabel('Valor')
        plt.title('Comunicación CAN')
        plt.show()
