"""Room Model"""

import discord
import rethinkdb
import typing as t
from panel import Panel

UserList = t.Optional[t.List[discord.User]]


class Room(discord.CategoryChannel):
    """Represents a private room on @rcade"""

    def _init_(self, owner: discord.User, name: str=None,
               game: str=None, is_nsfw: bool=False,
               is_private: bool=True, has_voice: bool=True,
               image: str=None, cover: str=None, *members: discord.User):

        # Basic Setup
        self.owner = owner
        if name:
            self.name = name
        else:
            self.name = f"{owner.name}'s Room"
        self.game = game
        self.members = [member for member in members]

        # Settings
        self.is_nsfw = is_nsfw
        self.is_private = is_private
        self.has_voice = has_voice

        # Cosmetic
        if image:
            self.image = image
        else:
            self.image = owner.avatar
        self.cover = cover  # Unimplemented Patreon Feature

        # Components
        self.panels = [Panel()]
        if game:
            self.panels.append(Panel(game))
        self.groups = {}

    async def delete(self):
        """Deletes room."""
        ...

    async def add_members(self, *members: discord.User) -> UserList:
        """Adds members to room."""
        ...

    async def change_game(self):
        """Changes room's game."""
        ...

    async def change_name(self, name: str=None):
        """Changes the name of the room."""
        ...

    async def manage_groups(self, **groups: UserList):
        """Manages game-based team or user channels."""
        ...
