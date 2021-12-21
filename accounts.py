import json
from pathlib import Path

def addScholar(file, ronin_address, discordId):
    discordId = str(discordId)
    ronin_address = str(ronin_address).lower().replace('ronin:', '0x').strip()

    scholar_details = {
        'roninAddress': ronin_address,
        'discordId': discordId
    }

    path = Path(file)

    if path.is_file():
        # file exist append existing file
        with open(file, 'r+') as file:
            # load existing data into a dict
            file_data = json.load(file)

            # check if discord id or ronin already exist
            for ids in file_data['scholars']:
                if discordId in ids['discordId'] or \
                        ronin_address in ids['roninAddress']:
                    return 'Failed to add: discordId or ronin address already exist'

            # join new data with file_data inside scholars
            file_data['scholars'].append(scholar_details)
            # set files current position at offset
            file.seek(0)

            # convert back to json
            json.dump(file_data, file)
    else:
        # create the json file

        scholar_details = {
            "scholars": [
                {
                    'roninAddress': ronin_address,
                    'discordId': discordId
                }
            ]
        }

        with open(file, 'w') as json_file:
            json.dump(scholar_details, json_file)

    return ''


def getRoninAddressByDiscordId(jsonfile, discordId, senderDiscordId=0):
    if Path(jsonfile).is_file():
        with open(jsonfile, 'r+') as file:
            file_data = json.load(file)

            for ids in file_data['scholars']:
                if discordId in ids['discordId']:
                    return ids['roninAddress']

            if senderDiscordId == 0:
                for ids in file_data['scholars']:
                    if senderDiscordId in ids['discordId']:
                        return ids['roninAddress']

            print('Failed to find ronin address link to the discord accpount')

            return ''
