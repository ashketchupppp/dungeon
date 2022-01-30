
from utils import Coordinate
import map as _map
import enum
from eventbus import EventBus, EventType
from functools import partial

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

class GameState:
  def __init__(self):
    self.map = _map.Map()
    self.entities = [
      Player(Coordinate(23, 23)),
      Character(pos=Coordinate(x=20, y=11))
    ]
    self.turnNo = 0

  def __getitem__(self, pos: Coordinate):
    ''' Returns a tuple of items at the location '''
    return self.getTileAtPos(pos), self.getEntityAtPos(pos)

  def step(self):
    ''' Go through all entities queued actions and run them if they are valid. '''
    for e in self.entities:
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
    for action in EntityActions:
      if self.validateAction(action, entity):
        validActions.append(action)
    return validActions

  def executeAction(self, action: dict, entity: Entity):
    if action['type'] in [EntityActions.MOVE_LEFT, EntityActions.MOVE_RIGHT, EntityActions.MOVE_DOWN, EntityActions.MOVE_UP]:
      self.moveEntity(entity, action['type'].value)

  def validateAction(self, actionType: EntityActions, entity: Entity):
    if actionType in [EntityActions.MOVE_LEFT, EntityActions.MOVE_RIGHT, EntityActions.MOVE_DOWN, EntityActions.MOVE_UP]:
      return self.validateMoveAction(actionType, entity)

  def validateMoveAction(self, actionType: EntityActions, entity):
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