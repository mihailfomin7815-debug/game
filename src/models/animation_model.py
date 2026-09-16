"""Модель звезды и 3D-проекции для звёздного поля"""

import random
import math

STAR_COLORS = [
    (255, 255, 255),
    (200, 220, 255),
    (255, 200, 150),
]


class Star:
    """Звезда в трёхмерном пространстве"""

    def __init__(self, max_depth):
        """Инициализирует звезду"""
        self.max_depth = max_depth
        self.color = random.choice(STAR_COLORS)
        self.base_size = random.uniform(0.5, 2.0)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.prev_sx = None
        self.prev_sy = None
        self.reset(new=True)

    def reset(self, new=False):
        """Перерождает звезду в новой случайной позиции
        Если new = True — случайная глубина (для первого запуска)
        Если new = False — максимальная глубина (звезда далеко)
        """

        self.x = random.uniform(-1000, 1000)
        self.y = random.uniform(-1000, 1000)

        if new:
            self.z = random.uniform(1, self.max_depth)

        else:
            self.z = self.max_depth
        self.prev_sx = None
        self.prev_sy = None

    def project(self, focal_length, cx, cy):
        """Проецирует 3D-координаты на 2D-экран"""

        if self.z <= 0:
            return None

        factor = focal_length / self.z
        sx = self.x * factor + cx
        sy = self.y * factor + cy
        return sx, sy

    def update(self, speed, dt, dir_x, dir_y, cx, cy, focal_length=300.0):
        """Обновляет позицию звезды за один кадр"""
        projected = self.project(focal_length, cx, cy)

        if projected is not None:
            self.prev_sx, self.prev_sy = projected

        else:
            self.prev_sx = None
            self.prev_sy = None

        self.z -= speed * dt * 60
        self.x -= dir_x * speed * dt * 40
        self.y -= dir_y * speed * dt * 40

        if self.z <= 0.5:
            self.reset()

    def get_screen_radius(self):
        """Вычисляет радиус звезды на экране"""
        depth = 1.0 - self.z / self.max_depth
        return max(1, int(self.base_size * depth * 4 + 0.5))

    def get_brightness(self):
        """Вычисляет яркость звезды от 0.1 до 1.0"""
        depth = 1.0 - self.z / self.max_depth
        return max(0.1, depth)

    def get_depth(self):
        """Возвращает нормализованную глубину от 0 до 1"""
        return 1.0 - self.z / self.max_depth

    def get_trail_length(self, focal_length, cx, cy):
        """Вычисляет длину следа в пикселях."""

        if self.prev_sx is None or self.prev_sy is None:
            return 0.0
        projected = self.project(focal_length, cx, cy)

        if projected is None:
            return 0.0

        sx, sy = projected
        dx = sx - self.prev_sx
        dy = sy - self.prev_sy
        return math.sqrt(dx * dx + dy * dy)
