import arcade
import random
import math
import sys
import time
import numpy as np

from .tile import Tile
from .utils.tile_image_gen import generate_image


DEFAULT_TILE_LEN = 100


class GameView(arcade.View):
    def __init__(self, window: arcade.Window, tiles: int):
        super().__init__(window=window)
        self.window.set_size(tiles*100, tiles*100)

        self.tiles_list = arcade.SpriteList()
        self.board = np.zeros((tiles, tiles), dtype=np.int32)
        self.prev_board = None

        self.tiles = tiles
        self.preloaded_textures = []

        self._tmp_direction = None

    def setup(self):
        self.window.ui_manager.purge_ui_elements()

        for i in range(2):
            m = (random.randint(0, self.tiles-1), random.randint(0, self.tiles-1))
            while self.board[m[0]][m[1]] != 0:
                m = (random.randint(0, self.tiles-1), random.randint(0, self.tiles-1))
            self.board[m[0]][m[1]] = 2

        self.preloaded_textures.append(generate_image(0))

        k = 2
        while k <= 2048:
            self.preloaded_textures.append(generate_image(k))
            k *= 2

    def _get_scale(self):
        width, height = self.window.get_size()
        return (width/self.tiles)/100

    def gen_tiles(self):
        scale = self._get_scale()
        q = DEFAULT_TILE_LEN

        self.tiles_list = arcade.SpriteList()

        for row in range(self.tiles):
            for col in range(self.tiles):
                if (v := self.board[row][col]) != 0:
                    val = int(math.log(v, 2))
                else:
                    val = 0
                texture = arcade.Texture(f"{row},{col}", self.preloaded_textures[val])
                x = scale*q*col + (scale*q)/2
                y = self.window.height - (scale*q*row + (scale*q)/2)

                t = Tile(texture=texture, center_x=x, center_y=y, scale=scale)
                self.tiles_list.append(t)

    def _move(self, direction: str):
        if direction not in ("left", "right", "up", "down"):
            raise Exception("Unknown direction.")

        self.prev_board = self.board.copy()

        if direction == "left":
            b = self.board

        elif direction == "up":
            b = np.rot90(self.board, k=1)

        elif direction == "right":
            b = np.rot90(self.board, k=2)

        elif direction == "down":
            b = np.rot90(self.board, k=3)

        else:  # For pycharm not to warn me "refrence before assignment", though I already prevented that.
            return

        combined = []

        for r in range(self.tiles):
            for c in range(self.tiles):
                if not c == 0:
                    for i in list(reversed(range(0, c))):
                        if b[r][i] == 0:
                            b[r][i] = b[r][i + 1]
                            b[r][i + 1] = 0
                        elif b[r][i] == b[r][i + 1] and (r, i) not in combined and (r, i+1) not in combined:
                            print(b[r][i], b[r][i+1])
                            b[r][i] = b[r][i + 1] * 2
                            b[r][i + 1] = 0
                            combined.append((r, i))
                        else:
                            break

        k = 0 if direction == "left" else 3 if direction == "up" else 2 if direction == "right" else 1
        self.board = np.rot90(b, k=k)
        print(self.board)
        time.sleep(0.1)

    def _gen_tile(self):
        available_tiles = [(r, c) for r in range(self.tiles) for c in range(self.tiles) if self.board[r][c] == 0]
        print(available_tiles)
        self.board[(n := random.choice(available_tiles))[0]][n[1]] = np.random.choice([2, 4], p=[0.8, 0.2])

    def _check_death(self):
        for b in (self.board, np.rot90(self.board)):
            for row in b:
                cache = None
                for val in row:
                    if val == cache:
                        return False
                    else:
                        cache = val
        return True

    def _check_win(self):
        return 2048 in [i for row in self.board for i in row]

    def _undo(self):
        if self.prev_board is not None:
            self.board = self.prev_board.copy()
            self.prev_board = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

        self.setup()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.BACKSPACE:
            self._undo()
            return

        if symbol in (arcade.key.LEFT, arcade.key.A, arcade.key.H):
            d = "left"
        elif symbol in (arcade.key.UP, arcade.key.W, arcade.key.K):
            d = "up"
        elif symbol in (arcade.key.DOWN, arcade.key.S, arcade.key.J):
            d = "down"
        elif symbol in (arcade.key.RIGHT, arcade.key.D, arcade.key.L):
            d = "right"
        else:
            return

        self._move(d)
        self._gen_tile()
        if self._check_death():
            time.sleep(1)
            print("lose, gg")
            sys.exit()
        if self._check_win():
            time.sleep(1)
            print("win, gg")
            sys.exit()

    def on_draw(self):
        arcade.start_render()

        self.gen_tiles()
        self.tiles_list.draw()
