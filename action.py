from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this the objects needed to determine its scope

        `engine` is the scope this action is being performed in.

        'entity' is the object performing the action.Action

        this method must be overridden by Action subclasses
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class ActionWithDir(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError

class MeleeAction(ActionWithDir):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_at_location(dest_x, dest_y)
        if not target:
            return # No entity to attack

        print(f"You poked {target.name} in the eyes, how rude.")

class MovementAction(ActionWithDir):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
                return # Destination is out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
                return # Destination is blocked by tile
        if engine.game_map.get_blocking_at_location(dest_x,dest_y):
                return # Destination is blocked by entity

        entity.move(self.dx, self.dy)

class BumpAction(ActionWithDir):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)