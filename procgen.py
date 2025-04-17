from __future__ import annotations

import random
from typing import Tuple, Iterator, TYPE_CHECKING, List

import tcod

import entity_factory
from game_map import GameMap
import tile_type

if TYPE_CHECKING:
    from entity import Entity

class RegularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self) ->Tuple[int, int]:
        center_x = int ((self.x1 + self.x2) / 2)
        center_y = int ((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2d array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RegularRoom) -> bool:
        """Return True if this room overlaps with another room"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def hallway(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: #50% Chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x1, y2
    else:
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1

    # generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((x2, y2), (corner_x, corner_y)).tolist():
        yield x, y


def place_entities(
            room: RegularRoom, dungeon: GameMap, max_enemy: int,
    ) -> None:
        num_of_enemy = random.randint(0, max_enemy)

        for i in range(num_of_enemy):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                if random.random() < 0.8:
                    entity_factory.pikeman.spawn(dungeon, x, y)
                else:
                    entity_factory.longsword.spawn(dungeon, x, y)


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        max_enemy_per_room: int,
        player: Entity,
) -> GameMap:
    """Generate a new dungeon map"""
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RegularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(3, dungeon.width - room_width - 1)
        y = random.randint(3, dungeon.height - room_height - 1)

        # "Room" class makes rectangles easier to work with
        new_room = RegularRoom(x, y, room_width, room_height)

        # Run through other rooms and see if they intersect with one another
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
        # This room doesn't intersect then this room is valid


        # Dug out the room inner area
        dungeon.tiles[new_room.inner] = tile_type.floor

        if len(rooms) == 0:
            # First room where player starts
            player.x, player.y = new_room.center
        else: # ALl rooms after the first
            # Dig out a tunnel between this room and then the previous one
            for x, y in hallway(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_type.floor

        place_entities(new_room, dungeon, max_enemy_per_room)

        # Finally, append the new room to the list
        rooms.append(new_room)


    return dungeon