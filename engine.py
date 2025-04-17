from typing import Iterable, Any

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
    def __init__(self, event_handle: EventHandle, game_map: GameMap, player: Entity):
        self.event_handle = event_handle
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_enemy(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print("Is it my turn yet.")

    def handle_event(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
         #   self.handle_enemy_turns()

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


        context.present(console)

        console.clear()