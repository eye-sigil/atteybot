import discord
from discord.ext import commands
import typing as t
import traceback
from models import rooms


class ManageRooms(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.conn

    @commands.command(pass_context=True, name='create')
    async def create_room(self, ctx,
                          members: commands.Greedy[discord.Member] = [],
                          name: t.Optional[str] = None):

        message = await ctx.send(":typing: Creating room...")

        room = rooms.Room(
            owner=ctx.author, name=name, members=members)

        await room.construct(ctx.guild)

        await message.edit(content="Room created!")

    @commands.command(pass_context=True, name='delete')
    async def delete_room(self, ctx):
        # TODO Call a wipe and then delete from memory
        ...


def setup(bot):
    bot.add_cog(ManageRooms(bot))
