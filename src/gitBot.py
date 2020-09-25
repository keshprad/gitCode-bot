import re
import requests
import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("I'm ready!")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def code(ctx, *, url):
    api_url = find_api_url(url)
    code = get_code(api_url)
    await ctx.send(f"**Here's the code:** ```{code}```")


def get_code(url):
    res = requests.get(url)
    code = res.text
    return code


def find_api_url(github_url):
    exclusions = ['https://', 'github.com/', 'github.com']
    url_data = re.sub('|'.join(exclusions), '', github_url)
    url_data = url_data.split(sep='/')

    file = {"user": url_data[0], "repo": url_data[1], "branch": url_data[3], "file_path": '/'.join(url_data[4:])}

    api_url = f"https://raw.githubusercontent.com/{file['user']}/{file['repo']}/{file['branch']}/{file['file_path']}"
    return api_url


bot.run(open("../bot_token", "r").read())
