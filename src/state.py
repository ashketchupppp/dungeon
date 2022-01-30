
from fileinput import close
from functools import partial

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from utils import Coordinate, dictFind
import map as _map
import enum
from eventbus import EventBus, EventType

class EntityAction(enum.Enum):
  MOVE_LEFT = Coordinate(-1, 0)
  MOVE_RIGHT = Coordinate(1, 0)
  MOVE_UP = Coordinate(0, -1)
  MOVE_DOWN = Coordinate(0, 1)
  MELEE_ATTACK = 'MELEE_ATTACK'
  
MOVE_ACTIONS = [
  EntityAction.MOVE_LEFT,
  EntityAction.MOVE_RIGHT,
  EntityAction.MOVE_DOWN,
  EntityAction.MOVE_UP
]
MOVE_ACTION_COORDS = [action.value for action in MOVE_ACTIONS]
ATTACK_ACTIONS = [
  EntityAction.MELEE_ATTACK
]
MELEE_RANGE = 2

class Entity:
  def __init__(self, pos: Coordinate):
    self.pos = pos
    self.actionQueue = []
  
  def queueAction(self, actionType: EntityAction, data = {}):
    self.actionQueue.append({ 'type': actionType, 'data': data })

  def nextAction(self):
    try:
      return self.actionQueue.pop()
    except IndexError:
      pass

class Character(Entity):
  def __init__(self, pos = Coordinate(0, 0), hp = 10, ap = 1):
    super().__init__(pos)
    self.hp = hp
    self.ap = ap

  def attack(self, target):
    target.hp -= self.ap

class Player(Character):
  eventsToActions = {
    EventType.MOVE_LEFT: EntityAction.MOVE_LEFT,
    EventType.MOVE_RIGHT: EntityAction.MOVE_RIGHT,
    EventType.MOVE_DOWN: EntityAction.MOVE_DOWN,
    EventType.MOVE_UP: EntityAction.MOVE_UP,
    EventType.MELEE_ATTACK: EntityAction.MELEE_ATTACK
  }

  @classmethod
  def getEventFromAction(self, action: EntityAction):
    return dictFind(Player.eventsToActions, action)

  def __init__(self, pos: Coordinate):
    super().__init__(pos=pos)
    for ac in Player.eventsToActions:
      EventBus.registerSubscriber(ac, partial(self.queueAction, Player.eventsToActions[ac]))

class NPC(Character):
  def __init__(self, pos=Coordinate(0, 0)):
      super().__init__(pos)

  def process(self, gameState):
    ''' Uses the current game state to return an action '''
    validActions = gameState.getValidActions(self)
    action = None
    if EntityAction.MELEE_ATTACK in validActions:
      nearestEntity = gameState.getNearestEntity(self.pos, excludeList=[self])
      self.attack(nearestEntity)

    elif set(validActions) <= set(MOVE_ACTIONS):
      matrix = gameState.map.toPathfindMatrix()
      grid = Grid(matrix=matrix)

      playerPos = gameState.getPlayer().pos
      start = grid.node(self.pos.x, self.pos.y)
      end = grid.node(playerPos.x, playerPos.y)

      finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
      path, runs = finder.find_path(start, end, grid)
      direction = Coordinate(*path[1]) - self.pos
      action = MOVE_ACTIONS[MOVE_ACTION_COORDS.index(direction)]
    return action

class GameState:
  def __init__(self):
    self.map = _map.Map()
    self.entities = [
      Player(Coordinate(23, 23)),
      NPC(pos=Coordinate(x=20, y=11))
    ]
    self.turnNo = 0

  def __getitem__(self, pos: Coordinate):
    ''' Returns a tuple of items at the location '''
    return self.getTileAtPos(pos), self.getEntityAtPos(pos)

  def step(self):
    ''' Go through all entities queued actions and run them if they are valid. '''
    for e in self.entities:
      if type(e) == NPC:
        e.queueAction(e.process(self))
      nextAction = e.nextAction()
      if nextAction:
        if self.validateAction(nextAction['type'], e):
          self.executeAction(nextAction, e)
    self.turnNo += 1

  def getPlayer(self):
    try:
      return [e for e in self.entities if type(e) == Player][0]
    except IndexError:
      return None

  def moveEntity(self, entity, d_pos):
    entity.pos += d_pos

  def getValidActions(self, entity: Entity):
    ''' Returns a list of valid actions for entity '''
    validActions = []
    for action in EntityAction:
      if self.validateAction(action, entity):
        validActions.append(action)
    return validActions

  def executeAction(self, action: dict, entity: Entity):
    if action['type'] in [EntityAction.MOVE_LEFT, EntityAction.MOVE_RIGHT, EntityAction.MOVE_DOWN, EntityAction.MOVE_UP]:
      self.moveEntity(entity, action['type'].value)

  def validateAction(self, actionType: EntityAction, entity: Entity):
    if actionType in MOVE_ACTIONS:
      return self.validateMoveAction(actionType, entity)
    elif actionType in ATTACK_ACTIONS:
      return self.validateAttackAction(actionType, entity)

  def validateAttackAction(self, actionType: EntityAction, entity):
    # determine if there is an entity within melee range
    closestEntity = self.getNearestEntity(entity.pos, excludeList=[entity])
    if entity.pos.dist(closestEntity.pos) > MELEE_RANGE:
      return False

    return True

  def validateMoveAction(self, actionType: EntityAction, entity):
    targetPos = actionType.value + entity.pos
    targetTile = self.getTileAtPos(targetPos)
    entityAtPos = self.getEntityAtPos(targetPos)
  
    if not targetTile:
      return False

    elif not targetTile.walkable:
      return False

    if entityAtPos:
      return False
    
    return True

  def getNearestEntity(self, pos: Coordinate, excludeList = []):
    ''' Returns the nearest entity to pos '''
    closest = None
    for e in self.entities:
      if not e in excludeList:
        if closest:
          closestPos = pos.whichIsCloser(e.pos, closest.pos)
          if pos == closestPos:
            closest = e
        else:
          closest = e
    return closest

  def getEntityAtPos(self, pos: Coordinate):
    ''' Returns an entity at pos, if there is one '''
    for i in self.entities:
      if i.pos == pos:
        return i

  def getTileAtPos(self, pos: Coordinate):
    ''' Returns the tiletype at pos '''
    try:
      return self.map[pos]
    except IndexError:
      pass