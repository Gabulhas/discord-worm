import json
from os import system
import re
import requests
from discord.ext import commands
import platform

data = {}

with open('config.json') as f:
    data = json.load(f)
token = data['token']

print(token)

codeRegex = re.compile("(https:\/\/discord.gg\/(.*))")

os = platform.system()

if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

print("STARTING DISCORD WORM")

bot = commands.Bot(command_prefix=".", self_bot=True)
total_servers = 0
ready = False
while 1:
    try:

        @bot.event
        async def on_message(ctx):
            global ready
            global total_servers
            if not ready:
                print("Login in as " + bot.user.name)
                print("Starting servers:" + str(len(bot.guilds)))
                total_servers = len(bot.guilds)
                ready = True
            if codeRegex.search(ctx.content):
                code = codeRegex.search(ctx.content).group(2)
                result = requests.post("https://discordapp.com/api/v6/invites/" + code,
                                       json={"channel_id": str(ctx.channel.id)},
                                       headers={'authorization': token}).json()
                if total_servers < len(bot.guilds):
                    print("Joined new guild: [" + result['guild']['name'] + "]")
                    print("Total servers:" + str(len(bot.guilds)))
        bot.run(token, bot=False)

    except:
        print("ERROR")
