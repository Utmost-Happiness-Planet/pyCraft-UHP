from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import NBTQueryPacket, BlockChangePacket, MultiBlockChangePacket
from minecraft.networking.packets.serverbound.play import QueryBlockNBTPacket
from .Player import PlayerSelf

"""
TODO:
    监听方块状态信息，完成对世界的实时建模。
"""


def register_connection(c: Connection, player: PlayerSelf):
    connection = c

    @connection.listener(QueryBlockNBTPacket,NBTQueryPacket)
    def trace_query(_p):
        print(_p)
        pass

    @connection.listener(BlockChangePacket, MultiBlockChangePacket)
    def trace_block_change(_p):
        print(_p)
        pass

    @connection.listener(QueryBlockNBTPacket,outgoing=True)
    def a(_p):
        print(_p)