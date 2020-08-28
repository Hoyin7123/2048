import arcade
from arcade import gui

from src.gameview import GameView
from src.otherviews import MenuView


def main():
    window = arcade.Window(1000, 1000, resizable=True)
    window.ui_manager = gui.UIManager(window)
    window.show_view(MenuView(window))
    arcade.run()


if __name__ == "__main__":
    main()
