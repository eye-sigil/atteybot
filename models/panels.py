import discord
# import rethinkdb
import typing as t
from models import panels
import peewee



class Panel(peewee.Model):
    """Represents a panel channel in an @rcade room."""
    
    class Meta:
        database = peewee.db('atteybot.db')

    def __init__(self, channel: discord.TextChannel):
        self.channel = channel

    def add_settings(self, structure: dict):
        """Adds setting to panel and channel."""
        # TODO This stuff lol
        ...

    async def delete(self):
        """Deletes panel and relevant rethinkdb entries."""
        await self.channel.delete()
