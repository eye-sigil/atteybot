import discord
from discord import commands
import traceback
import peony
import models


class ManageRooms:

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.conn

    @commands.command(pass_context=True)
    def create_room(self, ctx, name: str,
                    *members: discord.User) -> models.Room:

        category = ctx.author.guild.create_category(name=name)
        room = models.Room(
            members, category=category, owner=ctx.author, name=name)

        return room
