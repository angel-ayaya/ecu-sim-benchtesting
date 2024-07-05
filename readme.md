# CAN Simulator and Visualizer
================================

This project provides a CAN (Controller Area Network) simulator and visualizer using Python. The simulator sends and receives CAN messages, and the visualizer displays the received messages in a graphical format.

## Features
------------

### CAN Message Simulation

* Send and receive CAN messages using the `can` library
* Supports multiple arbitration IDs and data patterns
* Configurable message frequency and delay

### Message Reception and Validation

* Receive CAN messages and validate their contents
* Supports multiple expected data patterns
* Displays validation results in the console

### Graphical Visualization

* Displays received CAN messages in a graphical format using `matplotlib`
* Plots message timestamps and values
* Supports customizable plot settings

### User Interface

* Provides a user-friendly interface for sending custom CAN messages using `tkinter`
* Allows users to input arbitration ID and data values
* Displays sent and received messages in a message log

### Threaded Implementation

* Uses threading to concurrently run the simulator, receiver, and visualizer
* Ensures efficient and responsive performance

## Usage
--------

### Running the Simulator and Visualizer

1. Run the `main.py` script to start the simulator and visualizer.
2. The simulator will start sending and receiving CAN messages.
3. The visualizer will display the received messages in a graphical format.
4. You can send custom messages using the user interface.
5. Press `Ctrl+C` to stop the simulator and visualizer.

### Testing CAN Communication

1. Run the `test_can_communication.py` script to test CAN communication.
2. The script will simulate CAN communication and validate the results.

## Components
--------------

### `can_simulator.py`

* Implements the CAN simulator using the `can` library
* Sends CAN messages with configurable arbitration IDs and data patterns

### `can_receiver.py`

* Implements the CAN receiver using the `can` library
* Receives CAN messages and validates their contents

### `visualizer.py`

* Implements the CAN visualizer using `matplotlib`
* Displays received CAN messages in a graphical format

### `main.py`

* Starts the simulator, receiver, and visualizer
* Provides a user interface for sending custom CAN messages

### `test_can_communication.py`

* Tests CAN communication using the simulator and receiver

## Requirements
---------------

### Python

* Python 3.x

### Libraries

* `can` library (install using `pip install python-can`)
* `matplotlib` library (install using `pip install matplotlib`)
* `tkinter` library (install using `pip install tk`)

## License
---------

This project is licensed under the MIT License. See `LICENSE` file for details.

## Author
---------

Angel Ayala