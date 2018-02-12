"""Room Object for @rcade"""

import discord


class Room:
    """Represents a private room on @rcade"""

    def _init_(self, owner: discord.User, name: str=None,
               game: str=None, nsfw: bool=False, **users):
        self.owner = owner
        if name:
            self.name = name
        else:
            self.name = f"{owner.name}'s Room'"