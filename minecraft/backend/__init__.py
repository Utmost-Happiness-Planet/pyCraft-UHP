# 用于维系玩家对象的感知
from minecraft.networking.connection import Connection

from . import trace_position
from .Player import Player


def register_backend(c: Connection):
    player = Player(c)
    trace_position.register_connection(c, player)
    return player
