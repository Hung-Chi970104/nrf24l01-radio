from machine import Pin, SPI
import struct

from nrf24l01 import NRF24L01

led = Pin(2, Pin.OUT)                # LED
btn = Pin(20, Pin.IN, Pin.PULL_DOWN)  # button press
csn = Pin(12, mode=Pin.OUT, value=1)  # chip select not
ce  = Pin(11, mode=Pin.OUT, value=0)  # chip enable

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
pipes = (b"\xd2\xf0\xf0\xf0\xf0", b"\xe1\xf0\xf0\xf0\xf0")

def setup():
    # Explicitly initialize SPI0 with your exact wiring
    spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
    
    # Pass the explicitly defined 'spi' object to the nRF constructor
    nrf = NRF24L01(spi, csn, ce, payload_size=4)
    
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()
    
    led.value(0)
    return nrf

def demo(nrf):
    state = 0 
    while True:
        if state != btn.value():
            state = btn.value()
            led.value(state)
            
            print("tx", state)
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("i", state))
            except OSError:
                print('message lost')
            nrf.start_listening()
            
        if nrf.any():
            buf = nrf.recv()
            got = struct.unpack("i", buf)[0]
            print("rx", got)
            led.value(got)

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes
    

nrf = setup()
auto_ack(nrf)
demo(nrf)
