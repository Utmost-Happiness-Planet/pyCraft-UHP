from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import PlayerPositionAndLookPacket, UpdateHealthPacket
from minecraft.networking.packets.serverbound.play import PositionAndLookPacket, ClientStatusPacket
from .Player import PlayerSelf


def register_connection(c: Connection, player: PlayerSelf):
    connection = c

    @connection.listener(PlayerPositionAndLookPacket)
    def print_position(_p):
        print("玩家定位：x=%f, y=%f,z=%f" % (_p.x, _p.y, _p.z))
        player.set_position([_p.x, _p.y, _p.z])
        player.set_rotation([_p.yaw, _p.pitch])

    @connection.listener(PositionAndLookPacket, outgoing=True)
    def print_outgoing_position(_p):
        player.set_position([_p.x, _p.feet_y, _p.z])
        player.set_rotation([_p.yaw, _p.pitch])

    @connection.listener(UpdateHealthPacket)
    def print_health(_p):
        player.set_health(_p.health, _p.food, _p.food_saturation)
        print("玩家血量：%f，饱食度：%d，饱腹度：%f" % (_p.health, _p.food, _p.food_saturation))

    @connection.listener(UpdateHealthPacket)
    def player_respawn(_p):
        if _p.health == 0:
            print('玩家已死亡，现已重生')
            respawn_packet = ClientStatusPacket()
            respawn_packet.action_id = 0
            c.write_packet(respawn_packet)
