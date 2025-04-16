# This is a sample Python script.

#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handler import EventHandle

def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "unifont_8x16.png", 16, 16, tcod.tileset.CHARMAP_CP437

    )

    event_handler = EventHandle()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@",	(255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "M", 	(126, 94, 19))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handle=event_handler, game_map=game_map, player=player)

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