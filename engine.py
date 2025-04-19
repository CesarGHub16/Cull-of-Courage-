from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import entity_factory
from input_handler import MainGameEventHandler
from message_log import MessageLog
from render_function import render_bar, render_names_at_mouse_pos

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handler import EventHandle

"""
ENGINE TO HANDLE DRAWING
"""

class Engine:
    game_map: GameMap


    def __init__(self, player: Actor):
        self.event_handle: EventHandle = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_pos = (0, 0)
        self.player = player

    def handle_enemy_turn(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=6,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=31, y=26, width=40, height=45)

        render_bar(
            console=console,
            current_value=self.player.fighter.HP,
            max_value=self.player.fighter.MAX_HP,
            total_width=20
        )

        render_names_at_mouse_pos(console=console, x=31, y=10, engine=self)