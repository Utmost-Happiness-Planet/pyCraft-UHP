"""
后端，通过对数据包的监听，维护玩家状态。
"""
from minecraft.networking.connection import Connection

from . import trace_player, trace_block, trace_player_other
from .Player import Player, PlayerSelf


def register_backend(c: Connection):
    """
    为一个连接注册一个后端并返回该连接的主体玩家对象。
    """
    player = PlayerSelf(c)
    c.add_player(player)
    trace_player.register_connection(c, player)
    trace_player_other.register_connection(c, player)
    trace_block.register_connection(c, player)
    return player
