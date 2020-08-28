import arcade
from arcade import gui
from tkinter.messagebox import showerror

from .gameview import GameView


class MenuView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.ui_manager = window.ui_manager

    def on_show_view(self):
        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

    def draw_elements(self):
        self.ui_manager.purge_ui_elements()

        w, h = self.window.get_size()
        text = gui.UILabel("Press Enter to start a game!\n\n\n"
                           "Input the number of the tiles below if you wish to change it.",
                           center_x=int(w/2),
                           center_y=int(h*(1/2)),
                           width=1000,
                           height=150,
                           align="center",
                           )

        self.ui_manager.add_ui_element(text)

        tiles_input_box = gui.UIInputBox(center_x=int(w/2), center_y=h*(2/5), width=100, text="4", id="tiles_input_box")

        self.ui_manager.add_ui_element(tiles_input_box)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            tiles_input_box = self.ui_manager.find_by_id("tiles_input_box")

            if not tiles_input_box.text.isdigit():
                showerror("Error", "Invalid numbers of tiles inputted!")
                return
            tiles = int(tiles_input_box.text)

            if tiles < 3 or tiles > 32:
                showerror("Error", "Too many or too much tiles inputted!")
                return

            self.window.show_view(GameView(self.window, tiles))

    def on_draw(self):
        arcade.start_render()

        self.draw_elements()

