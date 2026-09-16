"""Главный модуль приложения «Звёздное поле»"""

import pygame
from src.models.animation_model import Star
from src.renderers.renderer import Renderer
from src.widgets.controls import Controls


class App:
    """Главный класс приложения
    Создаёт окно, инициализирует звёзды и запускает игровой цикл"""

    WIDTH = 1000
    HEIGHT = 700
    NUM_STARS = 600
    MAX_DEPTH = 800.0
    FPS = 60

    def __init__(self):
        """Инициализирует Pygame и все компоненты."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        pygame.display.set_caption("Звездное поле")
        self.clock = pygame.time.Clock()

        self.cx = self.WIDTH // 2
        self.cy = self.HEIGHT // 2

        self.stars = [
            Star(self.MAX_DEPTH) for _ in range(self.NUM_STARS)
        ]
        self.renderer = Renderer(self.screen)
        self.controls = Controls(self.cx, self.cy, self.WIDTH)

    def run(self):
        """Запускает главный цикл приложения"""

        while self.controls.running:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.controls.process_events()
            self.controls.update(dt)

            for star in self.stars:
                star.update(
                    speed=self.controls.speed,
                    dt=dt,
                    dir_x=self.controls.dir_x,
                    dir_y=self.controls.dir_y,
                    cx=self.cx,
                    cy=self.cy,
                )

            self.renderer.clear()

            self.stars.sort(key=lambda s: -s.z)
            for star in self.stars:
                self.renderer.draw_star(star, self.cx, self.cy)

            self.renderer.draw_hud(self.controls.speed)
            pygame.display.flip()

        pygame.quit()