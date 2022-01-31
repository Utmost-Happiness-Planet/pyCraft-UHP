import math
import time

from minecraft.networking.connection import Connection
from minecraft.operation import move, chat


class Player:
    position = []
    rotation = []
    health = 0
    food = 0
    food_saturation = 0

    def __init__(self, connection: Connection):
        self.connection = connection

    def get_pos(self):
        return self.position

    def get_rotation(self):
        return self.rotation

    def set_pos(self, pos: list[3]):
        self.position = pos

    def set_rotation(self, rotation: list[2]):
        self.rotation = rotation

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
