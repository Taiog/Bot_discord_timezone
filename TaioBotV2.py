from sys import flags
from dotenv import load_dotenv
import discord
import datetime
import pytz
import os

load_dotenv()
tz_BR = pytz.timezone("America/Recife")
datetime_BR = datetime.datetime.now(tz_BR)
horaBR = ":flag_br:" + datetime_BR.strftime("%A - %d %B/%y - %I:%M%p")

tz_CA = pytz.timezone("America/Regina")
datetime_CA = datetime.datetime.now(tz_CA)
horaCA = ":flag_ca:" + datetime_CA.strftime("%A - %d %B/%y - %I:%M%p")

tz_SE = pytz.timezone("Europe/Amsterdam")
datetime_SE = datetime.datetime.now(tz_SE)
horaSE = ":flag_se:" + datetime_SE.strftime("%A - %d %B/%y - %I:%M%p")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.content == ".hora":
            await message.channel.send(horaBR)
            await message.channel.send(horaCA)
            await message.channel.send(horaSE)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(os.getenv("TOKEN"))
