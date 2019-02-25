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
                 cover: str = None, *members: UserList) -> models.Room:
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
        self.is_teamed = False  # y/n team rooms
        self.is_playered = False  # y/n player rooms

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

        return self

    async def construct(self, guild) -> models.Room:
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

            await self.main.set_permissions(
                i, read_messages=True, send_messages=True)

            await self.info.set_permissions(
                i, read_messages=True)

        await self.panel.set_permissions(
            self.owner, read_messages=True, send_messages=True)

        self.constructed = True  # Room is now in Discord

        return self

    async def wipe(self):
        """Wipes room data from database and guild."""

        print(f'[attey] deleting room {self.name}')

        # Guild
        for i in self.category.channels:
            await i.delete(reason='Room deleted.')
            print(f'[attey] deleting channel {i} in room {self.name}')

        await self.category.delete(reason='Room deleted.')

        # TODO Database
        ...

        print(f'[attey] finished wiping room {self.name}')

    async def add_members(self, *members: discord.User):
        """Adds members to room."""

        print(
            '[attey] adding {} to {}'.format(
                "".join([str(i) for i in members]),
                self.name))

        to_player = []

        for i in members:

            # Counting
            if i not in self.members:
                self.members += i
            else:
                continue  # Don't duplicaaaaate

            # Rooms
            await self.main.set_permissions(
                i, read_messages=True, send_messages=True)

            await self.info.set_permissions(
                i, read_messages=True)

            if self.is_playered:
                to_player.append(i)

            # TODO Database
            ...

        if to_player:
            await self.create_player_channels(to_player)
        # TODO Pass off to the game? Should the command or the caller do that?

    def change_game(self, game: models.Game):
        """Changes room's game."""
        # TODO Special stuff I decide games will want or need
        self.game = game

    async def change_name(self, name: str = None):
        """Changes the name of the room."""
        self.name = name
        await self.category.edit(name=name)

    async def create_teams(self, teams) -> dict:
        """Creates game-based team channels."""
        # NOTE Not running clean up - hidden role team games?

        self.is_teamed = True

        for team, players in teams:

            channel = await self.category.guild.create_text_channel(
                f'{team}',
                category=self.category)
            for i in players:
                await channel.set_permissions(
                    i, read_messages=True, send_messages=True)

            self.other_channels.append(channel)
            self.teams[channel] = players

        return self.teams

    async def create_player_channels(self, players) -> dict:
        """Creates game-based player channels."""
        # NOTE Not running clean up - hidden role team games?

        self.is_playered = True

        for i in players:

            channel = await self.category.guild.create_text_channel(
                f'{i.name}',
                category=self.category)
            await channel.set_permissions(
                i, read_messages=True, send_messages=True)

            self.other_channels.append(i)
            self.player_channels[channel] = i

        return self.player_channels


class Panel:
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
