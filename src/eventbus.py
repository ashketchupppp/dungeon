import enum
from utils import Coordinate

class EventType(enum.Enum):
  KEY_W = 'KEY_W'
  KEY_D = 'KEY_D'
  KEY_A = 'KEY_A'
  KEY_S = 'KEY_S'
  KEY_Q = 'KEY_Q'
  QUIT = 'QUIT'
  MOVE_LEFT = Coordinate(-1, 0)
  MOVE_RIGHT = Coordinate(1, 0)
  MOVE_UP = Coordinate(0, -1)
  MOVE_DOWN = Coordinate(0, 1)
  ENTITY_MOVE = 'ENTITY_MOVE'

class EventBus:
  class EventAlreadyExists(Exception):
    pass
  class EventDoesNotExist(Exception):
    pass

  events = dict([(k, []) for k in EventType])

  @classmethod
  def registerSubscriber(cls, _type, subscriberMethod):
    ''' Subscriber method should be a function with either 0 arguments or created by functools.partial '''
    if _type in cls.events:
      cls.events[_type].append(subscriberMethod)
    else:
      raise EventBus.EventDoesNotExist( _type)

  @classmethod
  def triggerEvent(cls, _type):
    if _type in cls.events:
      for subscriberMethod in cls.events[_type]:
        subscriberMethod()
    else:
      raise EventBus.EventDoesNotExist(_type)