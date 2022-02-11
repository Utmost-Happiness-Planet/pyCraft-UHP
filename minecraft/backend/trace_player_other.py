from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import SpawnPlayerPacket, EntityPositionDeltaPacket
from .Player import Player, PlayerSelf


def register_connection(c: Connection, player: PlayerSelf):
    connection = c

    """
    TODO:
        实时记录其他玩家的位置信息提交到player_list
    """

    @connection.listener(SpawnPlayerPacket)
    def player_set(_p):
        p = Player()
        p.set_id(_p.entity_id)
        p.set_uuid(_p.player_UUID)
        p.set_position([_p.x, _p.y, _p.z])
        p.set_rotation([_p.yaw, _p.pitch])
        c.add_player(p)
        print(f"玩家 {p.uuid} 出现，位置:x={_p.x} y={_p.y} z={_p.z} yaw={_p.yaw} pitch={_p.pitch}")
        print(_p.entity_id)

    # TODO：无法对齐服务器中坐标
    # @connection.listener(EntityPositionDeltaPacket)
    # def get_player_position(_p):
    #     if _p.delta_x_float != 0 and _p.delta_y_float != 0 and _p.delta_z_float != 0:
    #         for i in c.player_list:
    #             if c.player_list[i].get_id() == _p.entity_id:
    #                 c.player_list[i].set_position(
    #                     c.player_list[i] + [_p.delta_x_float, _p.delta_y_float, _p.delta_z_float])
    #                 print(f"{c.player_list[i].get_uuid()} - {[_p.delta_x_float, _p.delta_y_float, _p.delta_z_float]}")
