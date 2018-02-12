import discord
import traceback
import peony
import models


class ManageRooms:
    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.conn

    def create_room(self, user: discord.User, name: str,
                    game: str=None, nsfw: bool=False, **users) -> models.Room:
        ...
