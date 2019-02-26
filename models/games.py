import discord
# import rethinkdb
import typing as t
from models import games
import peewee


class Game(peewee.Model):
    """Model for a game to run in an @rcade room."""
    
    class Meta:
        database = peewee.db('atteybot.db')

    ...  # LOOOOOOONG way to go until this is implemented
