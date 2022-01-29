
from utils import Coordinate
import map as _map
import enum
from eventbus import EventBus, EventType

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
    EventBus.registerSubscriber(EventType.KEY_A, lambda x: self.queueAction(EntityActions.MOVE_LEFT))
    EventBus.registerSubscriber(EventType.KEY_D, lambda x: self.queueAction(EntityActions.MOVE_RIGHT))
    EventBus.registerSubscriber(EventType.KEY_S, lambda x: self.queueAction(EntityActions.MOVE_DOWN))
    EventBus.registerSubscriber(EventType.KEY_W, lambda x: self.queueAction(EntityActions.MOVE_UP))

class GameState:
  def __init__(self):
    self.map = _map.Map()
    self.entities = [
      Player(Coordinate(0, 0)),
      Character(pos=Coordinate(x=10, y=10))
    ]
    self.turnNo = 0

  def step(self):
    ''' Go through all entities queued actions and run them if they are valid. '''
    for e in self.entities:
      nextAction = e.nextAction()
      if nextAction:
        if nextAction['type'] in [EntityActions.MOVE_LEFT, EntityActions.MOVE_RIGHT, EntityActions.MOVE_DOWN, EntityActions.MOVE_UP]:
          if self.validateMoveAction(nextAction['type'], e):
            self.moveEntity(e, nextAction['type'].value)
    self.turnNo += 1

  def moveEntity(self, entity, d_pos):
    entity.pos += d_pos

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