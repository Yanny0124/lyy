"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple


class Facing(Enum):
    """Facing 我们定义为一个枚举类，用于定义方向。"""
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid:
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        """DO NOT EDIT THIS METHOD"""
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}

    @property
    def current_pos(self) -> Tuple[int, int]:
        """current_pos 属性的 getter，返回私有属性 _current_pos"""
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        """current_pos 属性的 setter（作为第 1 题留空）

        要求：
          - 接受一个长度为 2 的 tuple (x, y)
          - 若传入非 tuple 或长度不为 2，应抛出 TypeError
          - 将 x, y 强制转换为 int，检查是否超出了宽高范围，
            如果任何一个超出则将其限制在最大宽高范围即可
          - 处理后存入 self._current_pos
        """
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError
        x = max(0, min(int(value[0]), self.width - 1))
        y = max(0, min(int(value[1]), self.height - 1))
        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:
        """让机器人向当前方向走一格
        返回新的坐标 (x,y) 同时更新成员变量
        利用好上面的 setter
        以右为X轴正方向，上为Y轴正方向
        """
        x, y = self._current_pos
        d = self.current_direction
        if d == Facing.RIGHT:
            x += 1
        elif d == Facing.LEFT:
            x -= 1
        elif d == Facing.UP:
            y += 1
        elif d == Facing.DOWN:
            y -= 1
        self.current_pos = (x, y)
        return self._current_pos

    def turn_left(self) -> Facing:
        """让机器人逆时针转向
        返回一个新方向 (Facing.UP/DOWN/LEFT/RIGHT)
        """
        self.current_direction = Facing((self.current_direction.value + 1) % 4)
        return self.current_direction

    def turn_right(self) -> Facing:
        """让机器人顺时针转向"""
        self.current_direction = Facing((self.current_direction.value - 1) % 4)
        return self.current_direction

    def find_enemy(self) -> bool:
        """如果找到敌人（机器人和敌人坐标一致），就返回true"""
        return self._current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:
        """将当前位置记录到 position_history 字典中
        键(key)为步数 step，值(value)为当前坐标 self.current_pos
        例如：step=1 时，记录 {1: (0, 0)}
        """
        self.position_history[step] = self._current_pos

    def get_position_at_step(self, step: int) -> tuple:
        """从 position_history 字典中获取指定步数的坐标
        如果该步数不存在，返回 None
        """
        return self.position_history.get(step, None)


class AdvancedGrid(Grid):
    def __init__(self, width, height, enemy_pos):
        super().__init__(width, height, enemy_pos)
        self.steps = 0

    def move_forward(self) -> Tuple[int, int]:
        self.steps += 1
        return super().move_forward()

    def distance_to_enemy(self) -> int:
        x, y = self.current_pos
        xx, yy = self.enemy_pos
        return abs(x - xx) + abs(y - yy)