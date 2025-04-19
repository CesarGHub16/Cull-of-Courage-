from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_components import BaseComponent
from input_handler import GameOverHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

import color



class Fighter(BaseComponent):
    entity: Actor

    def __init__(self,
                 hp: int,
                 armor: int,
                 magicresist: int,
                 attackdamage: int,
                 attackpower: int,
                 ):
        self.HP = hp
        self.MAX_HP = hp
        self.AR = armor
        self.MR = magicresist
        self.AD = attackdamage
        self.AP = attackpower

    @property
    def hp(self) -> int:
        return self.HP

    @hp.setter
    def hp(self, value: int) -> None:
        self.HP = max(0, min(value, self.MAX_HP))
        if self.HP == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
            death_color = color.player_die
            self.engine.event_handle = GameOverHandler(self.engine)
        else:
            death_message = f"{self.entity.name} is dead!"
            death_color = color.enemy_die

        self.entity.char = chr(0x25)
        self.entity.color = (188, 188, 188)
        self.entity.block_movement = False
        self.entity.ai = None
        self.entity.name = f"Remains of {self.entity.name}."
        self.entity.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_color)