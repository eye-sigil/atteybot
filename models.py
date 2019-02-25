"""Models for the attey framework."""

import discord
import rethinkdb
import typing as t
import models

UserList = t.Optional[t.List[discord.User]]


class Room:
    """Represents a private room on @rcade"""

    def __init__(self, owner: discord.User,
                 name: str = None, game: str = None,
                 is_nsfw: bool = False, is_private: bool = True,
                 has_voice: bool = True, image: str = None,
                 cover: str = None, *members: UserList):
        """Creates initial info and model for Room."""

        # Basic Setup
        self.owner = owner
        if name:
            self.name = name
        else:
            self.name = f"{owner.name}'s Room"
        self.game = game
        self.members = [member for member in members]
        self.members.append(owner)

        self.constructed = False  # Room exists in system, not yet in Discord

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
        self.other_channels = []
        self.teams = {}  # Channel: UserList
        self.player_channels = {}  # Channel: User

    async def construct(self, guild):
        """Creates room inside of the discord server."""
        # TODO Database functionality, join channel broadcasting

        # Category
        self.category = await guild.create_category(
            self.name,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False)},
            nsfw=self.is_nsfw)

        # Channels
        # FIXME Clean this up at some point by doing this via loop
        self.main = await guild.create_text_channel(
            'main',
            category=self.category)

        self.panel = await guild.create_text_channel(
            'panel',
            category=self.category)

        self.info = await guild.create_text_channel(
            'info',
            category=self.category)

        # Permissions
        for i in self.members:
            self.main.set_permissions(
                i, read_messages=True, send_messages=True)
        self.panel.set_permissions(
            self.owner, read_messages=True, send_messages=True)

        self.constructed = True  # Room is now in Discord

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

        print(
            f'[attey] adding {"".join([str(i) for i in members])} to {self.name}'
        )

        for member in members:
            if member not in self.members:
                self.members += members

        for i in self.category.channels:
            for j in members:
                await i.set_permissions(
                    j, read_messages=True, send_messages=True)

    def change_game(self, game: models.Game):
        """Changes room's game."""
        # TODO Special stuff I decide games will want or need
        self.game = game

    async def change_name(self, name: str = None):
        """Changes the name of the room."""
        self.name = name
        await self.category.edit(name=name)

    async def create_teams(self, teams) -> dict:
        """Manages game-based team or user channels."""
        # NOTE Not testing for kwargs - command should do that
        # NOTE Also not running clean up - hidden role team games?

        for team, members in teams:

            i = self.category.guild.create_text_channel(
                f'{team}',
                category=self.category)
            for j in members:
                i.set_permissions(
                    j, read_messages=True, send_messages=True)

            self.other_channels.append(i)
            self.teams[i] = members

        return self.teams


class Panel(discord.TextChannel):
    """Represents a panel channel in an @rcade room."""

    def __init__(self, channel: discord.TextChannel, name: str = "room"):
        self.channel = channel
        self.name = name

    def add_setting(self):
        """Adds setting to panel and channel."""
        pass  # en why eye

    async def delete(self):
        """Deletes panel and relevant rethinkdb entries."""
        await self.channel.delete()


class Game:
    """Model for a game to run in an @rcade room."""

    ...  # LOOOOOOONG way to go until this is implemented
