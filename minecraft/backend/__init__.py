# 用于维系玩家对象的感知
from minecraft.networking.connection import Connection

from . import trace_player, trace_block, trace_player_other
from .Player import Player, PlayerSelf


def register_backend(c: Connection):
    player = PlayerSelf(c)
    c.add_player(player)
    trace_player.register_connection(c, player)
    trace_player_other.register_connection(c, player)
    trace_block.register_connection(c, player)
    return player
