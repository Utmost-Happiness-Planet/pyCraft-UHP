# 用于维系玩家对象的感知
from minecraft.networking.connection import Connection

from . import trace_position, trace_block
from .Player import Player


def register_backend(c: Connection):
    player = Player(c)
    trace_position.register_connection(c, player)
    trace_block.register_connection(c, Player)
    return player
