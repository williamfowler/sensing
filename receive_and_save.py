import os
import sys
import time
from LoRa import LoRa  # import LoRa module configured in LoRa.py

# begin receiving loop
with open("received_data.txt", "a") as file:
    while True:
        # Request for receiving new LoRa packet
        LoRa.request()
        # Wait for incoming LoRa packet
        LoRa.wait()

        # Read the received message
        message = ""
        while LoRa.available() > 1:
            message += chr(LoRa.read())
        counter = LoRa.read()

        # Print received message and counter
        print(f"Received: {message}  {counter}")

        # Print packet/signal status including RSSI, SNR, and signalRSSI
        print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))

        # Show received status in case CRC or header error occur
        status = LoRa.status() 
        if status == LoRa.STATUS_CRC_ERR:
            print("CRC error")
        elif status == LoRa.STATUS_HEADER_ERR:
            print("Packet header error")

        file.write(message)
        file.flush()  # Ensure data is written to the file

try:
    pass
except Exception as e:
    print(f"Error: {e}")
    LoRa.end()