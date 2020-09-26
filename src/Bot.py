import re
import os
import requests
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("I'm ready!")


@bot.command()
async def ping(ctx):
    await ctx.send(f"{round(bot.latency * 1000)}ms")


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)


@bot.command()
async def code(ctx, *, url):
    api_url, file_name = find_api_url(url)
    code = get_code(api_url)

    if len(code) <= 200:
        await ctx.send(f"**Here's the code:** ```{code}```")
    else:
        # write to file
        with open(file_name, "w") as file:
            file.write(code)

        # send file to Discord in message
        with open(file_name, "rb") as file:
            await ctx.send("Oh No!\nYour code was too long...\n\nMaybe try viewing your code as a file:",
                           file=discord.File(file, file_name))
            os.remove(file_name)


def get_code(url):
    res = requests.get(url)
    code = res.text
    return code


def find_api_url(github_url):
    exclusions = ['https://', 'github.com/', 'github.com']
    url_data = re.sub('|'.join(exclusions), '', github_url)
    url_data = url_data.split(sep='/')
    file_name = url_data[-1]

    file = {"user": url_data[0], "repo": url_data[1], "branch": url_data[3], "file_path": '/'.join(url_data[4:])}

    api_url = f"https://raw.githubusercontent.com/{file['user']}/{file['repo']}/{file['branch']}/{file['file_path']}"
    return api_url, "data/"+file_name


bot.run(os.environ['TOKEN'])
