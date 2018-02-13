"""Panel Model"""

import discord


class Panel(discord.TextChannel):
    """Represents a panel channel in an @rcade room."""

    def __init__(self, channel: discord.TextChannel, name: str="room"):
        self.channel = channel
        self.name = name

    def add_setting(self):
        """Adds setting to panel and channel."""
        ...

    async def delete(self):
        """Deletes panel and relevant rethinkdb entries."""
        await self.channel.delete()
