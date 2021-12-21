import os
from dotenv import load_dotenv

import requests

load_dotenv()
header_host = os.getenv('header_host')
header_api = os.getenv('header_api')

def getDailySLP(ronin_address, host_url, api_directory, api_key):
    ronin_address = ronin_address.lower().strip().replace('ronin:', '0x')

    url = "https://" + host_url + "/" + api_directory + "/" + ronin_address

    queryString = {'id': ronin_address}

    headers = {
        header_host: host_url,
        header_api: api_key
    }

    response = requests.request('GET', url, headers=headers, params=queryString)

    if response is None:
        return "Failed to retrieve gained slp for today. Try again later."

    data_json = response.json()
    dailySLP = 'Name: ' + str(data_json['leaderboard']['name']) + '\n' + \
               'Today: ' + str(data_json['slp']['todaySoFar']) + '\n' + \
               'Yesterday: ' + str(data_json['slp']['yesterdaySLP']) + '\n'

    print(dailySLP)

    return dailySLP
