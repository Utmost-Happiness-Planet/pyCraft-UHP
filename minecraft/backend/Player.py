import math
import time

from minecraft.networking.connection import Connection
from minecraft.operation import move, chat


class Player:
    def __init__(self):
        self.position = []
        self.rotation = []
        self.id = 0
        self.uuid = ''
        self.on_ground = True

    def get_position(self):
        return self.position

    def get_rotation(self):
        return self.rotation

    def get_id(self):
        return self.id

    def get_uuid(self):
        return self.uuid

    def get_ground(self):
        return self.on_ground

    def set_position(self, pos: list[3]):
        self.position = pos

    def set_rotation(self, rotation: list[2]):
        self.rotation = rotation

    def set_id(self, id):
        self.id = id

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_ground(self, on_ground):
        self.on_ground = on_ground

    def __add__(self, pos: list[3]):
        dest = self.get_position()
        ans = []
        for i in range(0, 3):
            ans.append(dest[i] + pos[i])
        return ans


class PlayerSelf(Player):

    def __init__(self, connection: Connection):
        super(PlayerSelf, self).__init__()

        self.connection = connection

        self.health = 0
        self.food = 0
        self.food_saturation = 0
        self.set_uuid(self.connection.auth_token.profile.id_)

    def get_health(self):
        return [self.health, self.food, self.food_saturation]

    def set_uuid(self, id_):
        # 拼接uuid
        self.uuid = '-'.join([id_[:7], id_[7:11], id_[11:15], id_[15:19], id_[19:]])

    def set_health(self, health: float, food: int, food_saturation: float) -> None:
        self.health = health
        self.food = food
        self.food_saturation = food_saturation

    def move_to(self, destination: list[3]):
        for i in range(0, len(destination)):
            if destination[i] == '~':
                destination[i] = self.position[i]
        # 先计算一下距离和三轴分别的距离差
        distance, each_diff = move.calculate_distance(self.position, destination)
        # 如果距离大于100就要分步移动了
        while distance > 100:
            step_pos = [self.position[i] + (each_diff[i] * 10 / (math.sqrt(distance))) for i in range(3)]
            move.player_move(self.connection, step_pos, self.rotation)
            print("移动中…坐标为: x=%f, y=%f, z=%f" % (self.position[0], self.position[1], self.position[2]))
            # 防止移动过快，因为我不知道移动判定中"速度"具体的算法，只能用延时来避免
            time.sleep(0.05)
            distance, each_diff = move.calculate_distance(self.position, destination)
        move.player_move(self.connection, destination, self.rotation)
        print("移动完成。坐标为: x=%f, y=%f, z=%f" % (self.position[0], self.position[1], self.position[2]))

    def rotate_to(self, rotation: list[2]):
        move.player_move(self.connection, self.position, rotation)
        print("旋转完成。朝向为: yaw=%f, pitch=%f" % (self.rotation[0], self.rotation[1]))

    def send_message(self, message):
        chat.send_message(self.connection, message)

    def query_block(self, position: list[3], id):
        for i in range(0, len(position)):
            if position[i] == '~':
                position[i] = int(self.position[i])
        block_query.query_block(self.connection,position, id)
