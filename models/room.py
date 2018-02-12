"""Room Object for @rcade"""

import discord
import rethinkdb


class Room:
    """Represents a private room on @rcade"""

    def _init_(self, owner: discord.User, name: str=None,
               game: str=None, is_nsfw: bool=False,
               is_private: bool=True, has_voice: bool=True,
               image: str=None, cover: str=None, *members: discord.User):
        self.owner = owner
        if name:
            self.name = name
        else:
            self.name = f"{owner.name}'s Room"
        self.game = game
        self.is_nsfw = is_nsfw
        self.is_private = is_private
        self.has_voice = has_voice
        if image:
            self.image = image
        else:
            self.image = owner.avatar
        self.cover = cover
        self.members = [member for member in members]

    async def delete(self):
        """Deletes room."""
        ...

    async def add_members(self, *members: discord.User):
        """Adds members to room."""
        ...
