import os
import sys
import time
from LoRaRX import LoRa  # import LoRa module configured in LoRa.py

# Define the headers
headers = "PM2.5 PM10.0 UV Ambient_Light Date Time\n"

# Function to write headers if the file is empty or doesn't contain them
def write_headers_if_needed(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(headers)
    else:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line != headers.strip():
                with open(file_path, "w") as file:
                    file.write(headers)

# Check and write headers if needed
file_path = "data.txt"
write_headers_if_needed(file_path, headers)

# Begin receiving loop
with open(file_path, "a") as file:
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
            if status == LoRa.STATUS_CRC_ERR: 
                print("CRC error")
            elif status == LoRa.STATUS_HEADER_ERR: 
                print("Packet header error")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

try:
    pass
except Exception as e:
    print(f"Error: {e}")
    LoRa.end()
