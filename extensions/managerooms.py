import discord
from discord.ext import commands
import traceback
import peony
import models


class ManageRooms:

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.conn

    @commands.command(pass_context=True)
    async def create_room(self, ctx, name: str,
                    *members: discord.User) -> models.Room:

        category = await ctx.author.guild.create_category(name=name)
        room = models.Room(
            members, category=category, owner=ctx.author, name=name)

        await room.construct()

        return room

def setup(bot):
    bot.add_cog(ManageRooms(bot))
