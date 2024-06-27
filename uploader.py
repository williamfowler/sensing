#############################################################################
#                         Author: William Fowler                            #
#                       Project: NCAR Weather Stations                      #
#                            Date: 6/27/2024                                #
#          Purpose: this file will read in data which has been              #
#          transmitted over LoRa and is of the format:                      #
#            <PM2.5> <PM10.0> <UV> <Light> <YYYY-MM-DD> <HH:MM:SS>\n        #
#          The data will be sent to the CHORDS visualization platform       #
#          using HTTP requests. The instrument_id, email, and api_key       #
#          variables must be assigned correctly according to the            #
#          configuration on CHORDS.                                         #
#############################################################################

import requests
import os
import pandas as pd

# Read data into a data_frame
df = pd.read_csv('data.txt', sep=' ')
 
# set these fields to the current info for your CHORDS account
CHORDS_url = "http://ec2-100-29-142-65.compute-1.amazonaws.com" # no trailing /
instrument_id = 1
user_email = "williamfowler04@gmail.com"
api_key = "YqhoPAPVxa8BsUWaJTtF"

def send_request(row):
    # create url with all required information
    url = CHORDS_url + \
    "/measurements/url_create?instrument_id=" + str(instrument_id) + \
    "&PM25=" + str(row['PM2.5']) + "&PM10=" + str(row['PM10.0']) + \
    "&UV=" + str(row['UV']) + "&AmbLight=" + str(row['Ambient_Light']) + \
    "&at=" + row['Date'] + "T" + row['Time'] + \
    "&email=" + user_email + "&api_key=" + api_key

    # send request
    response = requests.get(url=url)
    print(response)


# iterate through data_frame
df.apply(send_request, axis=1)

# when finished, delete the data so we don't sent duplicates
os.remove("data.txt")