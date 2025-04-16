import numpy as np #type: ignore
from tcod.console import Console

import tile_type

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_type.floor, order="F")

        self.tiles[30:34, 22] = tile_type.wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Return TRUE if x and y are inside the bounds of the map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
