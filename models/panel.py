"""Panel Model"""

import discord
from discord import commands


class Panel(discord.TextChannel):
    """Represents a panel channel in an @rcade room."""

    def __init__(self, name: str="room"):
        self.name = name
