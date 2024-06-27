import os
import sys
import time
from LoRaRX import LoRa  # import LoRa module configured in LoRa.py

# begin receiving loop
with open("data.txt", "a") as file:
    while True:
        try:
            # Request for receiving new LoRa packet
            LoRa.request()
            # Wait for incoming LoRa packet
            LoRa.wait()

            # Put received packet to message variable
            message = ""
            while LoRa.available() > 0:
                message += chr(LoRa.read())

            # Write received message to the file
            if message.strip():
                file.write(message)
                file.flush()

            # Print received message in serial
            print(f"Received: {message.strip()}")

            # Print packet/signal status including RSSI, SNR, and signalRSSI
            print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))

            # Show received status in case CRC or header error occur
            status = LoRa.status()
            if status == LoRa.STATUS_CRC_ERR: print("CRC error")
            elif status == LoRa.STATUS_HEADER_ERR: print("Packet header error")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

try:
    pass
except Exception as e:
    print(f"Error: {e}")
    LoRa.end()