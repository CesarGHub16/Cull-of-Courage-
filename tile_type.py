from typing import Tuple

import numpy as np #type: ignore

# Tile graphics
graphic_dt = np.dtype(
    [
        ("ch", np.int32), #unicode codepoint.
        ("fg", "3B"), #Three unassigned bytes for our RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used to define tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool), #True if the tile can be walked on.
        ("transparent", np.bool), #True if this tile doesn't block FOV.
        ("dark", graphic_dt), #Graphics for when this tile is not in the FOV.
        ("light", graphic_dt), #Graphics for when this tile IS in the FOV.
    ]
)

def new_tile(
        *, #Enforce the use of Keywords, so that the parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int],Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int],Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

#Shroud represents unexplored, unseen tiles.
SHROUD = np.array((ord(" "), (12, 12, 12), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x2D)), (12, 12, 12), (0, 0, 0)),
    light=(ord(chr(0x2D)), (193, 156, 0), (0, 0, 0)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(chr(0x2588)), (12, 12, 12), (0, 0, 0)),
    light=(ord(chr(0x2588)), (118, 118, 118), (0, 0, 0)),
)
vace = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(chr(0x38)), (12, 12, 12), (0, 0, 0)),
    light=(ord(chr(0x38)), (193, 156, 0), (0, 0, 0)),
)