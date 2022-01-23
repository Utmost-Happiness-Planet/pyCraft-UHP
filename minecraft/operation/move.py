from minecraft.networking.connection import Connection
from minecraft.networking.packets.serverbound.play import PositionAndLookPacket


def calculate_distance(start: list[3], end: list[3]):
    ans = 0
    for i in range(3):
        ans += (start[i] - end[i]) * (start[i] - end[i])
    return ans, [end[i] - start[i] for i in range(3)]


def player_move(connection: Connection, dest: list[3], rotation: list[2]):
    pos_packet = PositionAndLookPacket()
    pos_packet.x = dest[0]
    pos_packet.feet_y = dest[1]
    pos_packet.z = dest[2]
    pos_packet.yaw = rotation[0]
    pos_packet.pitch = rotation[1]
    pos_packet.on_ground = True
    connection.write_packet(pos_packet, force=True)
