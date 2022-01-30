from functools import partial
import enum

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from utils import Coordinate
from eventbus import EventType, EventBus
from state import GameState

class EntityActions(enum.Enum):
  MOVE_LEFT = Coordinate(-1, 0)
  MOVE_RIGHT = Coordinate(1, 0)
  MOVE_UP = Coordinate(0, -1)
  MOVE_DOWN = Coordinate(0, 1)

class Entity:
  def __init__(self, pos: Coordinate):
    self.pos = pos
    self.actionQueue = []
  
  def queueAction(self, actionType: EntityActions, data = {}):
    self.actionQueue.append({ 'type': actionType, 'data': data })

  def nextAction(self):
    try:
      return self.actionQueue.pop()
    except IndexError:
      pass

class Character(Entity):
  def __init__(self, pos = Coordinate(0, 0)):
    super().__init__(pos)

class Player(Character):
  def __init__(self, pos: Coordinate):
    super().__init__(pos=pos)
    EventBus.registerSubscriber(EventType.MOVE_LEFT, partial(self.queueAction, EntityActions.MOVE_LEFT))
    EventBus.registerSubscriber(EventType.MOVE_RIGHT, partial(self.queueAction, EntityActions.MOVE_RIGHT))
    EventBus.registerSubscriber(EventType.MOVE_DOWN, partial(self.queueAction, EntityActions.MOVE_DOWN))
    EventBus.registerSubscriber(EventType.MOVE_UP, partial(self.queueAction, EntityActions.MOVE_UP))

class NPC(Character):
  def __init__(self, pos=Coordinate(0, 0)):
      super().__init__(pos)

  def process(self, gameState: GameState):
    matrix = gameState.map.toPathfindMatrix()
    grid = Grid(matrix=matrix)

    start = grid.node(*tuple(self.pos))
    end = grid.node(*tuple(gameState.getPlayer().pos))

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))