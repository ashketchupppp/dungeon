from multiprocessing import Event
from eventbus import EventBus, EventType
from functools import partial

class Keybindings:
  bindings = {
    EventType.KEY_Q: EventType.QUIT,
    EventType.KEY_A: EventType.MOVE_LEFT,
    EventType.KEY_D: EventType.MOVE_RIGHT,
    EventType.KEY_S: EventType.MOVE_DOWN,
    EventType.KEY_W: EventType.MOVE_UP
  }

  mapKeyEventToKey = {
    EventType.KEY_Q: 'q',
    EventType.KEY_A: 'a',
    EventType.KEY_D: 'd',
    EventType.KEY_S: 's',
    EventType.KEY_W: 'w',
  }

  @classmethod
  def keyEventToKey(cls, evt):
    return cls.keyEventToKey[evt]

  @classmethod
  def bind(cls):
    ''' Sets up event listeners according to Keybindings.bindings '''
    for keybind in cls.bindings:
      EventBus.registerSubscriber(keybind, partial(EventBus.triggerEvent, cls.bindings[keybind]))

  @classmethod
  def action(cls, key: str):
    pass

  @classmethod
  def key(cls, action: EventType):
    pass
