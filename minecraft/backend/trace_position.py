from minecraft.networking.packets.clientbound.play import PlayerPositionAndLookPacket
from minecraft.networking.packets.serverbound.play import PositionAndLookPacket
from minecraft.networking.connection import Connection
from .Player import Player


def register_connection(c: Connection, player: Player):
    connection = c

    @connection.listener(PlayerPositionAndLookPacket)
    def print_position(_p):
        print("玩家定位：x=%f, y=%f,z =%f" % (_p.x, _p.y, _p.z))
        player.set_pos([_p.x, _p.y, _p.z])
        player.set_rotation([_p.yaw, _p.pitch])

    @connection.listener(PositionAndLookPacket, outgoing=True)
    def print_outgoing_position(_p):
        player.set_pos([_p.x, _p.feet_y, _p.z])
        player.set_rotation([_p.yaw, _p.pitch])
