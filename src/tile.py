import arcade


class Tile(arcade.Sprite):
    def __init__(self, texture: arcade.Texture, center_x: float, center_y: float, scale: float, *args, **kwargs):
        super().__init__(scale=scale,
                         center_x=center_x,
                         center_y=center_y,
                         *args, **kwargs)

        self.texture = texture
