from minecraft.networking.packets.clientbound.play import SpawnPlayerPacket
from minecraft.networking.connection import Connection
from .Player import Player


def register_connection(c: Connection, player: Player):
    connection = c

    @connection.listener(SpawnPlayerPacket)
    def print_position(_p):
        print(_p)
