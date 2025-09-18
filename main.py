TOKEN = ""
PREFIX = 'r!'

import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def load_extensions():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN, reconnect=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

    await bot.change_presence(activity=discord.Streaming(name="TN Tech Role Bot", type=1, url="https://www.twitch.tv/tntechesports"))

if __name__ == '__main__':
    asyncio.run(main())