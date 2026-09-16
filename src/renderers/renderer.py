"""Модуль отрисовки звёзд, следов и HUD"""

import pygame
from src.models.animation_model import Star


class Renderer:
    """Отрисовщик звёздного поля"""

    FOCAL_LENGTH = 300.0

    def __init__(self, screen):
        """Инициализирует отрисовщик"""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)

    def clear(self):
        """Заливает экран тёмным фоном"""
        self.screen.fill((0, 0, 5))

    def draw_star(self, star, cx, cy):
        """Рисует одну звезду и ее след"""
        if star.z <= 0:
            return

        projected = star.project(self.FOCAL_LENGTH, cx, cy)

        if projected is None:
            return

        sx, sy = projected
        width = self.screen.get_width()
        height = self.screen.get_height()

        if not (-50 < sx < width + 50 and -50 < sy < height + 50):
            return

        depth = star.get_depth()
        radius = star.get_screen_radius()
        bright = star.get_brightness()

        r = min(255, int(star.color[0] * bright))
        g = min(255, int(star.color[1] * bright))
        b = min(255, int(star.color[2] * bright))
        color = (r, g, b)

        self._draw_trail(star, sx, sy, r, g, b, radius, depth)

        pygame.draw.circle(
            self.screen, color, (int(sx), int(sy)), radius
        )

        if radius >= 3:
            core = (
                min(255, r + 60),
                min(255, g + 60),
                min(255, b + 60),
            )
            pygame.draw.circle(
                self.screen, core,
                (int(sx), int(sy)), max(1, radius // 2)
            )

    def _draw_trail(self, star, sx, sy, r, g, b, radius, depth):
        """Рисует след звезды"""
        if star.prev_sx is None or depth <= 0.3:
            return

        dx = sx - star.prev_sx
        dy = sy - star.prev_sy
        dist = (dx * dx + dy * dy) ** 0.5

        if 1 < dist < 80:
            trail_color = (r // 2, g // 2, b // 2)
            pygame.draw.line(
                self.screen, trail_color,
                (int(star.prev_sx), int(star.prev_sy)),
                (int(sx), int(sy)),
                max(1, radius // 2),
            )

    def draw_hud(self, speed):
        """Рисует информационный текст поверх звёзд"""
        lines = [
            f"Скорость: {speed:.1f}  (W/S)",
            "Мышь — направление движения",
        ]
        for i, text in enumerate(lines):
            surface = self.font.render(text, True, (0, 180, 100))
            self.screen.blit(surface, (10, 10 + i * 22))
