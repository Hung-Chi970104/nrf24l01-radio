from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

# 1. Your exact hardware setup
spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
csn = Pin(5, mode=Pin.OUT, value=1)
ce = Pin(6, mode=Pin.OUT, value=0)

# 2. Initialize the nRF24L01 module
nrf = NRF24L01(spi, csn, ce)

# 3. Setup the communication pipe
# Use the exact same 5-byte address as the receiver
address = b"Node1"
nrf.open_tx_pipe(address)

print("Transmitter active! Sending data...\n")

counter = 0

# 4. Loop and send messages
while True:
    # Create a simple message and convert it to bytes
    message = f"Ping {counter}"
    byte_message = message.encode('utf-8')
    
    try:
        # send() blocks until the receiver sends back an "Acknowledgment" (ACK) packet
        nrf.send(byte_message)
        print(f"Success! Sent: {message}")
    except OSError:
        # If no ACK is received from the listener, the library throws an OSError
        print(f"Failed to send: {message} (No acknowledgment from receiver)")
        
    counter += 1
    time.sleep(1)