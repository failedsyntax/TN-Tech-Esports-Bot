import discord
import os
from discord.ext import commands

class ReactionRoles(commands.Cog):
    user: discord.ClientUser

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 380753007098200067
        self.role_message_id = os.getenv("MESSAGE_ID")
        self.emoji_to_role = {
            "<:RainbowSix:900234557498990622>": 846571945159032872,
            "<:Valorant:880879256551424070>": 700597533013180438,
            "<:Fortnite:900235734152278016>": 821858664343142400,
            "<:LeagueofLegends:900235482825392138>": 597586913745960961,
            "<:RocketLeague:900232811292815412>": 597586842489061408,
            "<:CallofDuty:900237164460269568>": 617108992568590346,
            "<:Overwatch:900231928400211980>": 597586889213476901,
            "<:Minecraft:900241564633284619>": 597586986806542336,
            "<:CounterStrike:900236233257652255>": 616088831103336452,
            "<:Destiny:900241572526948353>": 883434693800919050,
            "<:FGC:1168590138624987256>": 1145736575729279086,
            "<:RivalsEmoji:1407191892826918963>": 1407189137164861511,
            "<:mariokart:1278746613304524912>": 1276348551923896372,
            "<:Smite:900234278665879574>": 617108509418323987,
            "<:ApexLegends:900234821534613534>": 846571214922973264,
            #"<:Dota:900232187742412811>": 0
        }

    @commands.command(name="rr_setup", hidden=True)
    @commands.is_owner()
    async def setup_reaction_message(self, ctx):

        thumbnail_embed = discord.Embed(
            color= 0x4B2680,
            url="https://images-ext-1.discordapp.net/external/XQ50yWcA6sQeMMHYdh9TCKSEujeh-hriTlZVcImcwVc/https/i.ibb.co/Jj3zTsr/ROLE-SELECT-2.png"
        )

        thumbnail_embed.set_image(url="https://images-ext-1.discordapp.net/external/XQ50yWcA6sQeMMHYdh9TCKSEujeh-hriTlZVcImcwVc/https/i.ibb.co/Jj3zTsr/ROLE-SELECT-2.png")

        target_channel = self.bot.get_channel(self.channel_id)
        if target_channel is None:
            return

        try:
            message = await target_channel.fetch_message(self.role_message_id)
        except discord.NotFound:
            print(f'Message with ID {self.role_message_id} not found! | Sending new original message!')
            message = await target_channel.send(embed=thumbnail_embed)

            for emoji_string in self.emoji_to_role.keys():
                await message.add_reaction(emoji_string)

            self.role_message_id = message.id
            await ctx.send(message=f"Please save the new message id to the Railway variable! {self.role_message_id}")
        except Exception as e:
            print(e)
        else:
            await ctx.send(message=f"{message.author.mention}, the reaction role message already exists!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.emoji.message_id, self.role_message_id)
        print(payload.message_id == self.role_message_id)
        if payload.message_id != self.role_message_id:
            return

        # Variables
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)
        role_id = self.emoji_to_role.get(emoji)

        # Validity checking
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                return
            except Exception as e:
                print(e)
                return

        if guild is None:
            return

        if member.bot:
            return

        if role_id is None:
            return

        role = guild.get_role(role_id)

        if role is None:
            try:
                role = await guild.fetch_role(role_id)
            except discord.NotFound:
                print(f"Role {role_id} not found")
                return
            except Exception as e:
                print(f"Error fetching role {role_id}: {e}")
                return

        if role and (role not in member.roles):
            try:
                await member.add_roles(role)
            except discord.Forbidden as e:
                print(f"Unable to give role, check bot role permissions | {e}")
            except Exception as e:
                print(f"Error adding {role} to {member}: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.role_message_id:
            return

        # Variables
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)
        role_id = self.emoji_to_role.get(emoji)

        # Validity checking
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                return
            except Exception as e:
                print(e)
                return

        if guild is None:
            return

        if member.bot:
            return

        if role_id is None:
            return

        role = guild.get_role(role_id)

        if role is None:
            try:
                role = await guild.fetch_role(role_id)
            except discord.NotFound:
                print(f"Role {role_id} not found")
                return
            except Exception as e:
                print(f"Error fetching role {role_id}: {e}")
                return

        if role and (role in member.roles):
            try:
                await member.remove_roles(role)
            except discord.Forbidden as e:
                print(f"Unable to remove role, check bot role permissions | {e}")
            except Exception as e:
                print(f"Error adding {role} to {member}: {e}")

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))