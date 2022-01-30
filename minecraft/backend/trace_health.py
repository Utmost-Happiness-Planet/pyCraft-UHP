from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import UpdateHealthPacket
from minecraft.networking.packets.serverbound.play import ClientStatusPacket
from .Player import Player


def register_connection(c: Connection, player: Player):
    connection = c

    @connection.listener(UpdateHealthPacket)
    def print_health(_p):
        player.update_health(c, _p.health, _p.food, _p.food_saturation)
        print("玩家血量：%f，饱食度：%d，饱腹度%f" % (_p.health, _p.food, _p.food_saturation))

    @connection.listener(UpdateHealthPacket)
    def respawn(_p):
        if _p.health == 0:
            respawn_packet = ClientStatusPacket()
            respawn_packet.action_id = 0
            c.write_packet(respawn_packet)