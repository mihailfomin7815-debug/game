"""Модуль обработки пользовательского ввода"""

import pygame


class Controls:
    """Обработчик клавиатуры и мыши
    Хранит текущее состояние скорости и направления,
    обновляемое каждый кадр из событий Pygame"""

    MIN_SPEED = 0.0
    MAX_SPEED = 40.0
    SPEED_STEP = 10.0

    def __init__(self, cx, cy, width):
        """Инициализирует контроллер"""
        self.cx = cx
        self.cy = cy
        self.half_width = width / 2
        self.speed = 5.0
        self.dir_x = 0.0
        self.dir_y = 0.0
        self.running = True

    def process_events(self):
        """Обрабатывает очередь событий Pygame"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.running = False

    def update(self, dt):
        """Обновляет скорость и направление"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.speed = min(
                self.MAX_SPEED,
                self.speed + self.SPEED_STEP * dt,
            )

        if keys[pygame.K_s]:
            self.speed = max(
                self.MIN_SPEED,
                self.speed - self.SPEED_STEP * dt,
            )

        mx, my = pygame.mouse.get_pos()
        self.dir_x = (mx - self.cx) / self.half_width
        self.dir_y = (my - self.cy) / self.half_width
