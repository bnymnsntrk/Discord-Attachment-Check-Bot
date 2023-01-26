import datetime
import discord
import json

channel_list = []


class MyClient(discord.Client):

    async def on_ready(self):
        print('sa'.format(client))

    async def on_message(self, message):

        if message.author == self.user:
            return

        if message.author.guild_permissions.administrator:
            if message.content == "$silicibot listeyi sıfırla":
                channel_list.clear()
                await message.channel.send(f"Kontrol edilecek kanallar listesi temizlendi")
                return

            if message.content.startswith("$silicibot"):
                command = message.content.split(" ")
                i = 1
                while i < len(command):
                    channel_list.append(command[i])
                    i += 1
                await message.channel.send(f"Kontrol edilecek kanallar: {', '.join(channel_list)}")
                # print(f"kanal: <#{message.channel.id}>, liste: {channel_list[0]}")
            return

        if any(chn in f"<#{message.channel.id}>" for chn in channel_list) and not message.attachments:
            if not (message.content.startswith('https://') or message.content.startswith('http://')):
                await message.delete()
                await message.author.timeout(datetime.timedelta(minutes=5), reason=None)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
try:
    with open('token.json', 'r') as file:
        token = file.read()
    dict = json.loads(token)
    bot_token = str(dict[0]["token"])
except Exception as e:
    print(e)

client.run(bot_token)