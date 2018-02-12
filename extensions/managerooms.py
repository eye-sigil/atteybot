import discord
from discord import commands
import traceback
import peony
import models


class ManageRooms:

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.conn

    @commands.command()
    def create_room(self, owner: discord.User, name: str,
                    game: str=None, nsfw: bool=False,
                    **members: discord.User) -> models.Room:
        room = models.Room(
            members, owner=owner, name=name, game=game, nsfw=nsfw)

        return room
