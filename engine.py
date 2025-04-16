from typing import Set, Iterable, Any

from numpy.version import release
from tcod.context import Context
from tcod.console import Console

from action import EscapeAction, MovementAction
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

    def handle_event(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
                    self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, entity.color)

        context.present(console)

        console.clear()