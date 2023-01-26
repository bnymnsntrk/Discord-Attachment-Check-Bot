import datetime
import discord
import json

channel_list = []


class MyClient(discord.Client):

    async def on_ready(self):
        print('sa'.format(client))  # connected

    async def on_message(self, message):

        if message.author == self.user:  # don't check bot itself
            return

        if message.author.guild_permissions.administrator:  # only admin can give commands to bot
            if message.content == "$silicibot listeyi sıfırla":  # reset the current channel list
                channel_list.clear()
                await message.channel.send(f"Kontrol edilecek kanallar listesi temizlendi")
                return

            if message.content.startswith("$silicibot"):  # to add channels to list, message must start with this
                command = message.content.split(" ")
                i = 1  # i starts from 1 since the first word is $silicibot
                while i < len(command):
                    channel_list.append(command[i])  # each channel added to channel list
                    i += 1
                await message.channel.send(f"Kontrol edilecek kanallara eklendi: {', '.join(channel_list)}")
                # print(f"kanal: <#{message.channel.id}>, liste: {channel_list[0]}")
            return

        if any(chn in f"<#{message.channel.id}>" for chn in channel_list) and not message.attachments:
            if not (message.content.startswith('https://') or message.content.startswith('http://')):
                await message.delete()  # delete the message since it doesn't include attachment or link
                await message.author.timeout(datetime.timedelta(minutes=5), reason=None)  # apply 5min timeout to user


# initialization
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
try:
    with open('token.json', 'r') as file:  # pull the bot token from json file
        token = file.read()
    dict = json.loads(token)
    bot_token = str(dict[0]["token"])
except Exception as e:
    print(e)

client.run(bot_token)
