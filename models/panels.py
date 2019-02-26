import discord
# import rethinkdb
import typing as t
from models import panels




class Panel:
    """Represents a panel channel in an @rcade room."""

    def __init__(self, channel: discord.TextChannel):
        self.channel = channel

    def add_settings(self, structure: dict):
        """Adds setting to panel and channel."""
        # TODO This stuff lol
        ...

    async def delete(self):
        """Deletes panel and relevant rethinkdb entries."""
        await self.channel.delete()
