import discord
from discord.ext import commands
import time
import asyncio
import youtube_dl
import json
import os
from datetime import datetime

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

bot = commands.Bot(command_prefix='!')
path = 'https://www.youtube.com/watch?v=q6EoRBvdVPQ'

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
    print('>> Bot is online !')

    global data
    if os.path.isfile(os.path.join(os.getcwd(), "config.json")):
        data = None
        with open('config.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Data read Successful !")
    else:
        print("Data config read Failed !")
        # clients
        #  - "client ID"
        #    - "bgm"  >> file name or Youtube Link
        #    - "time" >> how much time music plays
        #    - "img"  >> Show Img
        data = {
            "FFmpeg" : 'path of ffmpeg',
            "clients":
            {
                "":{
                    "bgm": "",
                    "time": "",
                    "img":""
                    }
            }
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
    for client, intext in data["clients"].items():
        print(client, intext)
    for guild in bot.guilds:
        if guild.id == "GUILD ID":
            for channel in guild.text_channels:
                if channel.id == "CHANNEL ID":
                    global reply_channel
                    reply_channel = channel

@bot.command()
async def add_user(ctx, id, link, time, img=""):
    data["clients"][str(id)] = {
        "bgm": str(link),
        "time": str(time),
        "img" : img
    }
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

@bot.command()
async def add_subm(ctx, id, img):
    data["clients"][str(id)] = {
        "img": str(img)
    }
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

@bot.command()
async def update_context(ctx):
    global data
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print('>>> Updata seccusful <<<')

@bot.event
async def on_voice_state_update(member, before, after):
    new_channel = after.channel
    old_channel = before.channel

    if old_channel == None and new_channel is not None:
        if str(member.id) in data["clients"]:
            client = data["clients"][str(member.id)]
            await asyncio.sleep(1)
            await reply_channel.send('[{}] <@{}> is enter [{}] voic_channel! '.format(datetime.now().strftime("%H:%M:%S"), member.id, new_channel))
            if "img" in client:
                if client['img']:
                    await reply_channel.send(file=discord.File(client['img']))

            vch = bot.get_channel(after.channel.id)
            vc = await vch.connect()

            file = client["bgm"]
            if "https://www.youtube.com/" in file:
                file = await YTDLSource.from_url(url=file)
            vc.play(discord.FFmpegPCMAudio(executable=data["FFmpeg"], source=file))
            await asyncio.sleep(int(client["time"]))
            await vc.disconnect()


bot.run("BOT TOKEN") # Bot Token