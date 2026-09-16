from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

# 1. Your exact hardware setup
spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
csn = Pin(5, mode=Pin.OUT, value=1)
ce = Pin(6, mode=Pin.OUT, value=0)

# 2. Initialize the nRF24L01 module
# The library defaults to channel 46 and a payload size of 16 bytes
nrf = NRF24L01(spi, csn, ce)

# 3. Setup the communication pipe
# Both boards MUST use the exact same 5-byte address to talk to each other
address = b"Node1"
nrf.open_rx_pipe(0, address)
nrf.start_listening()

print("Receiver active! Listening for data...\n")

# 4. Loop and check for incoming messages
while True:
    if nrf.any(): # Check if the RX FIFO has data
        raw_bytes = nrf.recv()
        
        # The library pads short messages with null bytes (\x00), so we strip them
        message = raw_bytes.rstrip(b'\x00').decode('utf-8')
        print(f"Received: {message}")
        
    time.sleep_ms(10) # Tiny delay to keep the RP2040 from running at 100% CPU