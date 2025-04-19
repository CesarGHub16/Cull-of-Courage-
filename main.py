# This is a sample Python script.

#!/usr/bin/env python3
import copy

import tcod

from engine import Engine
import entity_factory
from input_handler import EventHandle
from procgen import generate_dungeon

def main():
    screen_width = 100
    screen_height = 80

    map_width = 100
    map_height = 75

    room_max_size = 8
    room_min_size = 6
    max_room = 13

    max_enemy_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "Alloy_rougeplus_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437

    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    event_handler = EventHandle()

    player = copy.deepcopy(entity_factory.player)

    game_map = generate_dungeon(
        max_rooms=max_room,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_enemy_per_room=max_enemy_per_room,
        player=player,
    )

    engine = Engine(event_handle=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Cull of Courage",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            event = tcod.event.wait()

            engine.handle_event(event)



if __name__ == '__main__':
    main()