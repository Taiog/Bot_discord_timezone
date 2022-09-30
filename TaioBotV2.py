from email import message
from mailbox import linesep
from operator import truediv
from sys import flags
from unittest import result
from dotenv import load_dotenv
import discord
import datetime
import pytz
import requests
import os
import json
import pymongo
from pymongo import MongoClient

load_dotenv()
cluster = MongoClient(os.getenv("MONGO"))
db = cluster["LinkList"]
collection = db["links_discord"]


def calculateTime(country, zone):
    time = pytz.timezone(zone)
    timenow = datetime.datetime.now(time)
    print(country + timenow.strftime("%A - %d %B/%y - %I:%M%p"))
    return country + timenow.strftime("%A - %d %B/%y - %I:%M%p")


cotacoes = requests.get(
    "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
)
cotacoes = cotacoes.json()
cotacao_dolar = "A cotação atual do dólar é R$" + cotacoes["USDBRL"]["bid"]

karderainfo = requests.get("https://api.tibiadata.com/v3/world/kardera")
karderainfo = karderainfo.json()
karderaplayers = karderainfo["worlds"]["world"]["players_online"]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.author == client.user:
            return

        if message.content == ".hora":
            await message.channel.send(
                calculateTime(":flag_br: ", "America/Recife")
                + os.linesep
                + calculateTime(":flag_ca: ", "America/Regina")
                + os.linesep
                + calculateTime(":flag_se: ", "Europe/Amsterdam")
            )

        if message.content == ".dolar":
            await message.channel.send(cotacao_dolar)

        if message.content == ".kardera":
            await message.channel.send(
                "Quantidade de players online em kardera: " + str(karderaplayers)
            )

        if message.content.startswith(".add"):
            linkmsg = message.content.split(".add ", 1)[1]
            post = {"link": linkmsg}
            collection.insert_one(post)
            await message.channel.send("Novo link foi adicionado")

        if message.content == ".linklist":
            results = collection.find()
            for result in results:
                print(result)
                await message.channel.send(result["link"])

        if message.content == ".commands":
            await message.channel.send(
                "Olá, esses são os meus comandos:"
                + os.linesep
                + " -> '.hora' - Para saber o horário atual no Brasil, Canadá(Regina) e na Suécia;"
                + os.linesep
                + " -> '.dolar' - Para saber a cotação do dolar em tempo real;"
                + os.linesep
                + " -> '.kardera' - Para saber quantas pessoas estão jogando no momento no desértico mundo de kardera;"
                + os.linesep
                + " -> Meu mais novo comando é um Favoritos, digite '.add (um link importante)' para salvar esse link importante no meu banco de dados, para consultá-los, basta digita '.linklist';"
            )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(os.getenv("TOKEN"))


# def calculateTime(country = '', zone = ''):
#    hora = datetime.datetime.now()
#
#   tz_BR = pytz.timezone("America/Recife")
#  datetime_BR = datetime.datetime.now(tz_BR)
#
#   tz_CA = pytz.timezone("America/Regina")
#  datetime_CA = datetime.datetime.now(tz_CA)
#
#   tz_SE = pytz.timezone("Europe/Amsterdam")
#  datetime_SE = datetime.datetime.now(tz_SE)
#
#
#  hora_string = hora.strftime("%A - %d %B/%y - %I:%M%p")
# horaUTC = ":united_nations:" + hora_string
# print(horaUTC)
#
#   horaBR = ":flag_br:" + datetime_BR.strftime("%A - %d %B/%y - %I:%M%p")
#  print(horaBR)
#
#   horaCA = ":flag_ca:" + datetime_CA.strftime("%A - %d %B/%y - %I:%M%p")
#  print(horaCA)
# horaSE = ":flag_se:" + datetime_SE.strftime("%A - %d %B/%y - %I:%M%p")
# print(horaSE)
