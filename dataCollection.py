from urllib import response
import requests
import pandas as pd
import numpy as np
import datetime

# Setting this option will print all collums of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth',None)

# several help functions
def getBoosterVersion(data):
    """
    Takes the dataset and uses the rocket column to call the API and append
    the data to the list
    """
    for x in data['rocket']:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])


def getLaunchSite(data):
    """
        Takes the dataset and uses the launchpad column to call
        API and append the data to the lists
    """
    for x in data['launchpad']:
        response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
        Longitude.append(response['longitude'])
        Latitude.append(response['latitude'])
        LaunchSite.append(response['name'])

def getPayloadData(data):
    """
        Takes the dataset and uses the payloads column to call the API
        and append the data to the lists
    """
    for load in data['payloads']:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

def getCoreData(data):
    """
        Takes the dataset and uses the cores column to call the API 
        and append the data to the lists  
    """
    # for core in data['cores']:
        # if core['core'] != None:
        #     response = requests.get("https://api.spacexdata.com/v4/cores"+core['core']).json()
        #     Block.append(response['block'])
        #     ReusedCount.append(response['reuse_count'])
        #     Serial.append(response['serial'])
        # else:
        #     Block.append(None)
        #     ReusedCount.append(None)
        #     Serial.append(None)
        # Outcome.append(str(core['landing_success'])+' '+ str(core['landing_type']))
        # Flights.append(core['flight'])
        # GridFins.append(core['gridfins'])
        # Reused.append(core['reused'])
        # Legs.append(core['legs'])
        # LandingPad.append(core['landpad'])
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

# spacex_url ="https://api.spacexdata.com/v4/launches/past"
# response = requests.get(spacex_url)
# print(response.content)
static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
res = requests.get(static_json_url).json()
# print(res.content)
data = pd.json_normalize(res)
# print(data.head(5))

# Lets take a subset of dataframe keeping only the features 
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Call getBoosterVersion
getBoosterVersion(data)

# Call getLaunchSite
getLaunchSite(data)

# Call getPayloadData
getPayloadData(data)

# Call getCoreData
getCoreData(data)

launch_dict = {'FlightNumber': list(data['flight_number']),\
    'Date': list(data['date']),\
    'BoosterVersion':BoosterVersion,\
    'PayloadMass':PayloadMass,\
    'Orbit':Orbit,\
    'LaunchSite':LaunchSite,\
    'Outcome':Outcome,\
    'Flights':Flights,\
    'GridFins':GridFins,\
    'Reused':Reused,\
    'Legs':Legs,\
    'LandingPad':LandingPad,\
    'Block':Block,\
    'ReusedCount':ReusedCount,\
    'Serial':Serial,\
    'Longitude': Longitude,\
    'Latitude': Latitude}

launch_df = pd.DataFrame([launch_dict])
launch_df2 = pd.DataFrame(launch_dict)
launch_df.to_csv('launch_df_list.csv')
launch_df2.to_csv('df2.csv')
# print(launch_df.describe())
