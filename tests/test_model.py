"""Тесты для математической модели звезды."""

import unittest
from src.models.animation_model import Star


class TestStarProjection(unittest.TestCase):
    """Тесты проекции и расчётов звезды."""

    def test_project_returns_none_when_behind(self):
        """Звезда за наблюдателем (z <= 0) не проецируется."""
        star = Star(max_depth=800)
        star.z = 0
        self.assertIsNone(star.project(300, 500, 350))

    def test_project_center_when_at_center(self):
        """Звезда в центре (x=0, y=0) проецируется в центр."""
        star = Star(max_depth=800)
        star.x = 0
        star.y = 0
        star.z = 100
        result = star.project(300, 500, 350)
        self.assertIsNotNone(result)
        sx, sy = result
        self.assertAlmostEqual(sx, 500.0)
        self.assertAlmostEqual(sy, 350.0)

    def test_closer_star_is_bigger(self):
        """Ближняя звезда имеет больший радиус."""
        far = Star(max_depth=800)
        far.z = 700
        near = Star(max_depth=800)
        near.z = 50
        self.assertGreater(
            near.get_screen_radius(),
            far.get_screen_radius(),
        )

    def test_brightness_range(self):
        """Яркость всегда в диапазоне [0.1, 1.0]."""
        star = Star(max_depth=800)
        for z in [1, 100, 400, 799]:
            star.z = z
            b = star.get_brightness()
            self.assertGreaterEqual(b, 0.1)
            self.assertLessEqual(b, 1.0)


if __name__ == "__main__":
    unittest.main()
