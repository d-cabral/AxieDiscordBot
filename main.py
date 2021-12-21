import discord
import os

from dotenv import load_dotenv

import utilityCommands as uc
import accounts as acc

client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

default_channel_id = int(os.getenv('Bot_Channel_ID'))
default_admin_only_channel_id = int(os.getenv('Bot_Channel_ID_Admin_Only'))
default_starting_char = os.getenv('Acceptable_Starting_Character')

public_proxy_axie_api_key = os.getenv('api_key')
public_proxy_axie_api_host_url = os.getenv('url_host_axie')
public_proxy_axie_api_directory = os.getenv('api_directory')

scholar_file = os.getenv('scholar_json_filename')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # validate the starting character of the message
    if not message.content.startswith(default_starting_char):
        return
    else:
        # Do check what command the user used.
        messageChannelID = message.channel.id
        messageUserID = message.author.id

        # validate channel where the message was sent
        # if default_channel_id == messageChannelID:
        #     await message.channel.send('its the correct chanel')

        if message.content.startswith(default_starting_char + '?'):
            await message.channel.trigger_typing()

            result = 'Please refer to the commands below: \n'
            result += '`' + default_starting_char + '?`: Displays the list of commands\n'
            result += '`' + default_starting_char + 'daily` or `' + default_starting_char + 'todaySLP`: Display yesterday and today\'s farmed SLP\n'
            result += '`' + default_starting_char + 'newScholar` <ronin Address> <discord ID>\n'

            await message.reply(result)

        if message.content == default_starting_char + 'test':
            await message.channel.send("Hello in Private Brother!")

        if message.content.startswith(default_starting_char + 'todaySLP') or\
                message.content.startswith(default_starting_char + 'daily'):

            ronin = ''

            if len(message.content.lower().split()) > 1:
                msg_split = message.content.lower().split()
                if len(msg_split[1]) >= 42 and len(msg_split[1]) <= 46:
                    ronin = str(msg_split[1]).lower().replace('ronin:', '0x').strip()
                else:
                    ronin = acc.getRoninAddressByDiscordId(scholar_file, str(msg_split[1]), senderDiscordId=messageUserID)
            else:
                ronin = acc.getRoninAddressByDiscordId(scholar_file, str(messageUserID))

            if len(ronin.strip()) == 0:
                # await message.reply('Insufficient permission. :x:')
                return

            await message.channel.trigger_typing()

            result = uc.getDailySLP(ronin_address=ronin, host_url=public_proxy_axie_api_host_url,
                                    api_directory=public_proxy_axie_api_directory, api_key=public_proxy_axie_api_key)
            print(result)
            await message.reply(result)

        if message.content.startswith(default_starting_char + 'newScholar'):

            await message.channel.trigger_typing()

            if default_admin_only_channel_id == messageChannelID:
                await message.reply('Insufficient command permission. Admin only')

            msg_split = message.content.lower().split()

            if msg_split is None:
                await message.reply('command Format: <' + default_starting_char + 'newScholar <ronin Address> <discord ID>')
            if len(msg_split[1]) < 42 or len(msg_split[1]) > 46:
                await message.reply('command Format: <' + default_starting_char + 'newScholar <ronin Address> <discord ID>')

            roninAddress = str(msg_split[1])
            discordId = str(msg_split[2])

            result = acc.addScholar(scholar_file, roninAddress, discordId)

            if len(result) > 0:
                await message.reply(result)
            else:
                await message.reply('ronin address: ' + roninAddress + ' linked to discordId: ' + discordId + ' successfully saved.')

@client.event
async def on_connect():
    print("Bot connected to the server!")
    channel = client.get_channel(919453045702656140)
    # await channel.send("Just connected to bot-commands!")


client.run(TOKEN)
