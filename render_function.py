from __future__ import annotations

from typing import TYPE_CHECKING

import color
from entity_factory import player

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_name_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(
        console: Console, current_value: int, max_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / max_value * total_width)

    console.draw_rect(x=0, y=70, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=70, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=70, string=f"HP: {current_value}/{max_value}", fg=color.bar_text
    )
    console.print(
        x=1, y=72, string=f"AR: {player.fighter.AR}", fg=color.bar_text
    )
    console.print(
        x=1, y=74, string=f"MR: {player.fighter.MR}", fg=color.bar_text
    )

def render_names_at_mouse_pos(
        console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_pos

    name_at_location = get_name_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=name_at_location)