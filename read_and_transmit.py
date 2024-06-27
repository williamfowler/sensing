# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import
import time
import board
import busio
import adafruit_ltr390 # uv sensor
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C # air quality sensor
from LoRaTX import LoRa # import LoRa module configured in LoRa.py
from datetime import datetime

reset_pin = None

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
aq_sensor = PM25_I2C(i2c, reset_pin)

print("Found air quality sensor")

# connect to uv sensor over i2c
i2c = board.I2C()
uv_sensor = adafruit_ltr390.LTR390(i2c)

print("Found uv sensor")

while True:
    time.sleep(1) # can change frequency of reading

    to_transmit = {}

    # collect reading from aq sensor
    try:
        aqdata = aq_sensor.read()
        to_transmit['aq_pm25'] = aqdata["pm25 standard"]
        to_transmit['aq_pm100'] =  aqdata["pm100 standard"]
    except RuntimeError:
        print("Could not read air quality sensor")
        continue

    # collect reading from uv sensor
    try:
        to_transmit['uv_value'] = uv_sensor.uvs
        to_transmit['ambient_light'] = uv_sensor.light
    except RuntimeError:
        print("Could not read uv sensor")
        continue

    # convert each character to integer representation (Unicdoe value)
    for metric in to_transmit:
        print(metric)
        message = str(to_transmit[metric]) # convert to string
        message = message.strip() + " " # add sentinel because converting from number
        messageList = list(message) # get list of characters
        for i in range(len(messageList)):
            messageList[i] = ord(messageList[i]) # convert to unicode value

        # transmit the values one at a time
        LoRa.beginPacket()
        LoRa.write(messageList, len(messageList))
        LoRa.endPacket()

        print(f"Transmitted: {message.strip()}")
        LoRa.wait()

         # Print transmit time and data rate
        print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))

        time.sleep(0.1)  # Small delay between transmissions

    # transmit the current date and time followed by a newline
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_message = current_time + "\n"
    current_time_list = list(current_time_message)
    for i in range(len(current_time_list)):
        current_time_list[i] = ord(current_time_list[i])

    LoRa.beginPacket()
    LoRa.write(current_time_list, len(current_time_list))
    LoRa.endPacket()

    print(f"Transmitted: {current_time.strip()}")
    LoRa.wait()

    # Print transmit time and data rate for the date and time transmission
    print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))