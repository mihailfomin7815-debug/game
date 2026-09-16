"""Точка входа в приложение «Звёздное поле»"""

from src.app import App


def main():
    """Создаёт экземпляр приложения и запускает главный цикл"""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
