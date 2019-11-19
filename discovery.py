import ciscosparkapi
import os
import sys
import json
import requests
import csv
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
import env_lab
import env_user

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

IND_Host = env_lab.IND['host']
IND_USER = env_lab.IND['username']
IND_PASSWORD = env_lab.IND['password']
IND_Port = env_lab.IND['port']
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic c3lzdGaW46QyFzY28xMjQ==",
            }

def create_url(path, controller_ip=IND_Host):
    """ Helper function to create a IND API endpoint URL
    """
    return "https://%s:%i/api/v1/%s" % (controller_ip, IND_Port, path)


def get_url(url):
    url = create_url(path=url)
    #print(url)
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    return response.json()


def list_discovery_profiles():
    return get_url("discovery-profiles")

def create_discovery_profiles(url):
    url = create_url(path=url)
    print(url)

    try:
        output = []
        with open('devices.csv', 'r') as f:
            reader = csv.DictReader(f)
            for records in reader:
                output.append(records)
        with open('RecordsJson.json','w')as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4)
        with open('RecordsJson.json', 'r') as infile:
            indata = json.load(infile)
        for data in indata:
            r = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
            print(r, r.text)

    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

def delete_discovery_profile(url):
    url = create_url(path=url)
    response = list_discovery_profiles()
    count = 0
    discovery_id = []
    while count < response['recordCount']:
        discovery_id.append(response['records'][count]['id'])
        count = count + 1
        data = {"ids": discovery_id}
    r = requests.delete(url, headers=headers, data=json.dumps(data), verify=False)
    #print(r, r.text)

def discovery_profile_scan():
    data = "{\n  \"action\": \"discovery\"\n}"
    response = list_discovery_profiles()
    count = 0
    while count < response['recordCount']:
        discovery_id = response['records'][count]['id']
        path = "discovery-profiles/" + str(discovery_id) + "/tasks"
        url = "https://%s:%i/api/v1/%s" % (IND_Host, IND_Port, path)
        requests.post(url, headers=headers, data=data, verify=False)
        count = count + 1
    print("Discovery Profile Scanning started, please check IND for devices found")

def print_discovery_profiles():
    response = list_discovery_profiles()
    print("{0:30}{1:17}{2:20}{3:30}".
        format("Discovery Profile Name","Start IP","End IP",
        "Access Profile Name"))
    message = spark.messages.create(roomId=env_user.SPARK_ROOM_ID, text="{0:30}{1:17}{2:20}{3:30}".
        format("Discovery Profile Name","Start IP","End IP",
        "Access Profile Name"))

    for profile in response['records']:
        print("{0:30}{1:17}{2:20}{3:10}".
            format(profile['name'],
                    profile['startIp'],
                    profile['endIp'],
                    profile['accessProfileName']))

        message = spark.messages.create(roomId=env_user.SPARK_ROOM_ID, text="{0:30}{1:17}{2:20}{3:30}".
            format(profile['name'],
                    profile['startIp'],
                    profile['endIp'],
                    profile['accessProfileName']))

if __name__ == "__main__":

    choice = input('Enter your choice\n\n 1: Print Discovery Profiles \n 2: Crete Discovery Profiles\n 3: Delete Discovery Profile \n 4: Scan Discovery Profiles\n')
    if choice == '1':
        print_discovery_profiles()
    elif choice == '2':
        create_discovery_profiles("discovery-profiles")
        print_discovery_profiles()
        print("Above Discovery Profiles were created")
        message = spark.messages.create(roomId=env_user.SPARK_ROOM_ID, text="Above Discovery Profiles were created")
    elif choice == '3':
        print_discovery_profiles()
        print("Above Discovery Profiles were deleted")
        delete_discovery_profile("discovery-profiles")
        message = spark.messages.create(roomId=env_user.SPARK_ROOM_ID, text="Above Discovery Profiles were deleted")
    else:
        discovery_profile_scan()
        message = spark.messages.create(roomId=env_user.SPARK_ROOM_ID, text="Discovery Profile Scanning started, please check IND for devices found")
