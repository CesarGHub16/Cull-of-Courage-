from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handler import EventHandle

"""
ENGINE TO HANDLE DRAWING
"""

class Engine:
    def __init__(self, entities: Set[Entity], event_handle: EventHandle, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handle = event_handle
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_event(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov() # Update FOV before player next action

    def update_fov(self) -> None:
        self.game_map.visable[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visable

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            # Only print entities in the FOV range
            if self.game_map.visable[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()