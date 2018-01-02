#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Bot Main'''

import traceback
import json
import raven
import rethinkdb as rethink
import sys
import discord
from discord.ext import commands
from discord.ext.commands import errors as commands_errors
from discord import utils as dutils

# INITIALIZE BOT #

class Bot(commands.Bot):
    '''Custom Bot Class that overrides the commands.ext one'''

    def __init__(self, **options):
        print('Performing initialization...\n')
        self.cmd_help = cmd_help
        with open('config.json') as f:
            self.config = json.load(f)
            self.prefix = self.config.get('BOT_PREFIX')
            self.version = self.config.get('VERSION')
            self.description = self.config.get('DESCRIPTION')
            self.integrations = self.config.get('INTEGRATIONS')
            self.owners = self.config.get('OWNERS')
            self.maintenance = self.config.get('MAINTENANCE')
        super.__init__(self.get_prefix,
                       description=self.description,
                       **options)
        self.remove_command("help")
        self.init_raven()
        # TODO rethinkdb structure - let ry handle
        # self.rdb =
        # self.rtables =
        # self.init_rethinkdb()
        print('Initialization complete.\n\n')

    async def get_prefix(self, bot, msg):
        return commands.when_mentioned_or(*self.prefix)(bot, msg)

    async def on_ready(self):
        app_info = await self.application_info()
        self.invite_url = dutils.oauth_url(app_info.id)
        print(
            f'Logged in as {self.user.name}\nInvite link: {self.invite_url}')
        await self.change_presence(
            game=discord.Game(
                name=f'{self.prefix[0]}help | Version {self.version}',
                type=0))
        self.load_extension('extensions.core')

    async def on_message(self, message):
        if message.author.bot and message.author.id not in self.integrations:
            return
        if message.author.id in self.config.get('BLOCKED'):
            return
        if message.author.id not in self.owners and self.maintenance:
            return
        await self.process_commands(message)

    def init_raven(self):
        print('Now initialising Sentry...\n')
        self.sentry = raven.Client(self.config['SENTRY'])
        print('Sentry initialised.\n')

    def find_command(self, cmdname: str):
        for i in self.commands:
            if i.name == cmdname:
                return i
        return False


async def cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(
            ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)
    for page in _help:
        await ctx.send(page)

bot = Bot()
print("bot created.\n")

# INITIALIZE BOT END #


@bot.listen("on_command_error")
async def on_command_error(ctx, exception):
    if isinstance(exception, commands_errors.MissingRequiredArgument):
        await cmd_help(ctx)

    elif isinstance(exception, commands_errors.CommandInvokeError):
        exception = exception.original
        _traceback = traceback.format_tb(exception.__traceback__)
        _traceback = ''.join(_traceback)
        embed_fallback = "ERROR: CONTACT @rcade ADMINS"

        error = discord.Embed(
            title="An error has occurred.",
            color=0xFF0000,
            description="This is (probably) a bug. This has been automatically reported, but give ry00001#3487 or taciturasa#4365 a friendly Gamer Nudge."
        )

        sentry_string = "{} in command {}\nTraceback (most recent call last):\n{}{}: {}".format(
            type(exception).__name__,
            ctx.command.qualified_name,
            _traceback,
            type(exception).__name__,
            exception)
        print(sentry_string)

        error.add_field(
            name="`{}` in command `{}`".format(
                type(exception).__name__, ctx.command.qualified_name),
            value="```py\nTraceback (most recent call last):\n{}{}: {}```".format(
                _traceback, type(exception).__name__, exception))

        ctx.bot.sentry.captureMessage(sentry_string)

        await ctx.send(embed_fallback, embed=error)

    elif isinstance(exception, commands_errors.CommandOnCooldown):
        await ctx.send(
            'This command is on cooldown. You can use this command in `{0:.2f}` seconds.'.format(
                exception.retry_after))
    else:
        ctx.send(exception)


@bot.command(aliases=['instructions'])
async def help(ctx, command: str = None):
    cmd = ctx.bot.find_command(command)
    helptext = await ctx.bot.formatter.format_help_for(
        ctx, cmd if cmd is not False else ctx.bot)
    helptext = helptext[0]
    try:
        await ctx.author.send(helptext)
        await ctx.send(":mailbox_with_mail: Check your DMs.")
    except discord.Forbidden:
        await ctx.send(helptext)
bot.get_command("help").hidden = True

print("Connecting...")
bot.run(bot.config['BOT_TOKEN'])
