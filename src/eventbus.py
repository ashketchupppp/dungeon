import enum

class EventType(enum.Enum):
  KEY_W = 'KEY_W'
  KEY_D = 'KEY_D'
  KEY_A = 'KEY_A'
  KEY_S = 'KEY_S'
  KEY_Q = 'KEY_Q'
  ENTITY_MOVE = 'ENTITY_MOVE'

class EventBus:
  class EventAlreadyExists(Exception):
    pass
  class EventDoesNotExist(Exception):
    pass

  events = dict([(k, []) for k in EventType])

  @classmethod
  def registerSubscriber(cls, _type, subscriberMethod):
    if _type in cls.events:
      cls.events[_type].append(subscriberMethod)
    else:
      raise EventBus.EventDoesNotExist( _type)

  @classmethod
  def triggerEvent(cls, _type, data={}):
    if _type in cls.events:
      for subscriberMethod in cls.events[_type]:
        if len(data):
          subscriberMethod(_type, data=data)
        else:
          subscriberMethod(_type)
    else:
      raise EventBus.EventDoesNotExist(str(_type.value))