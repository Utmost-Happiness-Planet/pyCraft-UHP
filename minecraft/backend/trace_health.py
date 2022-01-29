from minecraft.networking.packets.clientbound.play import UpdateHealthPacket
from minecraft.networking.connection import Connection
from .Player import Player


def register_connection(c: Connection, player: Player):
    connection = c

    @connection.listener(UpdateHealthPacket)
    def print_health(_p):
        print(_p)
