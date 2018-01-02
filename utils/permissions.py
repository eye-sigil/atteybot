from discord.ext import commands


def is_owner_check(ctx):
    return str(ctx.message.author.id) in ctx.bot.config.get('OWNERS')


def is_owner_or_gmod(ctx):
    return (
        str(ctx.message.author.id) in ctx.bot.config.get('OWNERS')) or (
        str(ctx.message.author.id) in ctx.bot.config.get('GLOBAL_MODS'))


def owner_id_check(bot, _id):
    return str(_id) in bot.config.get('OWNERS')


def owner():
    return commands.check(is_owner_check)


def owner_or_gmod():
    return commands.check(is_owner_or_gmod)
