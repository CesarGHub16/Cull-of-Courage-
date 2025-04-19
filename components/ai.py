from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

import entity_factory
from action import Action, MeleeAction, MovementAction, WaitAction
from components.base_components import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        No valid path -> return an empty list.
        """
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # If entity blocks movement and tile is walkable, increase path cost
            if entity.block_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=2)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        tcod_path = pathfinder.path_to((dest_x, dest_y))

        if len(tcod_path) <= 1:
            return []

        path = tcod_path[1:].tolist()  # Skip the starting point
        return [(x, y) for x, y in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []


    def perform(self) -> None:
        # Use engine reference through the entity's gamemap
        target = self.entity.gamemap.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance


        if entity_factory.swordman:
            if self.entity.gamemap.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    return MeleeAction(self.entity, dx, dy).perform()

                self.path = self.get_path_to(target.x, target.y)
        elif entity_factory.ranger:
            if self.entity.gamemap.visible[self.entity.x, self.entity.y]:
                if distance <= 4:
                    return MeleeAction(self.entity, dx, dy).perform()

                self.path = self.get_path_to(target.x, target.y)


        if entity_factory.swordman:
            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(
                    self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
                ).perform()

            return WaitAction(self.entity).perform()
        elif entity_factory.ranger:
            if self.path:
                dest_x, dest_y = self.path.pop(12)
                return MovementAction(
                    self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
                ).perform()

            return WaitAction(self.entity).perform()