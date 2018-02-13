"""Room Model"""

import discord
import rethinkdb
import typing as t

UserList = t.Optional[t.List[discord.User]]


class Room:
    """Represents a private room on @rcade"""

    def __init__(self, *members: discord.User, owner: discord.User,
               category: discord.CategoryChannel, name: str=None,
               game: str=None, is_nsfw: bool=False,
               is_private: bool=True, has_voice: bool=True,
               image: str=None, cover: str=None):

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
        self.category = category
        self.groups = {}

    async def construct(self):
        self.panel_channel = await self.category.guild.create_text_channel('panel', category=self.category)
        self.panels = [Panel(self.panel_channel)]
        if self.game:
            self.panels.append(Panel(self.panel_channel))

    async def delete(self):
        """Deletes room."""
        print(f'[attey] deleting room {self.name}')
        for i in self.category.channels:
            await i.delete(reason='Room deleted.')
            print(f'[attey] deleting channel {i} in room {self.name}')
        await self.category.delete(reason='Room deleted.')
        print(f'[attey] finished deleting room {self.name}')

    async def add_members(self, *members: discord.User) -> UserList:
        """Adds members to room."""
        print(f'[attey] adding {"".join([str(i) for i in members])} to {self.name}')
        self.members += members
        for i in self.category.channels:
            for j in members:
                await i.set_permissions(j, read_messages=True, send_messages=True)

    def change_game(self, game:str):
        """Changes room's game."""
        self.game = game

    async def change_name(self, name: str=None):
        """Changes the name of the room."""
        self.name = name 
        await self.category.edit(name=name)

    async def manage_groups(self, **groups: UserList):
        """Manages game-based team or user channels."""
        pass # nyi

class Panel(discord.TextChannel):
    """Represents a panel channel in an @rcade room."""

    def __init__(self, channel: discord.TextChannel, name: str="room"):
        self.channel = channel
        self.name = name

    def add_setting(self):
        """Adds setting to panel and channel."""
        pass #en why eye

    async def delete(self):
        """Deletes panel and relevant rethinkdb entries."""
        await self.channel.delete()

