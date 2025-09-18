from discord.ext import commands

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def find_extension(self, cog_name):
        for ext in list(self.bot.extensions):
            if ext.lower().endswith(f'.{cog_name.lower()}'):
                return ext
        return None


    @commands.command(name='load', hidden=True)
    @commands.is_owner()

    async def load(self, ctx, *, cog):
        """
        Command to load a module/cog
        Remember to use dot path (cogs.dev)
        """

        path = self.find_extension(cog)
        if not path:
            return await ctx.send(f'**Error:** {cog} not found')

        try:
            await self.bot.load_extension(path)
        except Exception as e:
            await ctx.send(f'**Error [{e.__class__.__name__}]:** {type(e).__name__}: {e}')
        else:
            await ctx.send(f'**Successfully loaded {path}!**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """
        Command to unload a module/cog
        Remember to use dot path (cogs.dev)
        """

        path = self.find_extension(cog)
        if not path:
            return await ctx.send(f'**Error:** {cog} not found')

        try:
            await self.bot.unload_extension(path)
        except Exception as e:
            await ctx.send(f'**Error [{e.__class__.__name__}]:** {type(e).__name__}: {e}')
        else:
            await ctx.send(f'**Successfully unloaded {path}!**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        """
        Command to reload a module/cog
        Remember to use dot path (cogs.dev)
        """

        path = self.find_extension(cog)
        if not path:
            return await ctx.send(f'**Error:** {cog} not found')

        try:
            await self.bot.unload_extension(path)
            await self.bot.load_extension(path)
        except Exception as e:
            await ctx.send(f'**Error [{e.__class__.__name__}]:** {type(e).__name__}: {e}')
        else:
            await ctx.send(f'**Successfully reloaded {path}!**')

async def setup(bot):
    await bot.add_cog(Developer(bot))
