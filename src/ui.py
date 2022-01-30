from functools import partial
from abc import ABC, abstractmethod
import curses

from keybinds import Keybindings
from map import LAND, WATER
from state import Character, Entity, GameState, EntityAction
from utils import Coordinate, strReplace, clamp
from state import Player, NPC
from keybinds import Keybindings
from eventbus import EventBus, EventType

class Renderable(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def render(self, dispArea):
    raise NotImplementedError

class Color:
  colors = {}
  colorKey = 1

  @classmethod
  def get(cls, fg, bg) -> int:
    if (fg, bg) in cls.colors:
      return cls.colors[(fg, bg)]
    else:
      cls.colors[(fg, bg)] = cls.colorKey
      curses.init_pair(cls.colorKey, fg, bg)
      cls.colorKey += 1
      return cls.colorKey - 1

class Pad:
  def __init__(self, pos: Coordinate, w, h):
    
    self.pad = curses.newpad(h + 1, w + 1)
    self.pos = pos
    self.w = w
    self.h = h

  def addstr(self, y, x, string, attrs=0):
    ''' addstr to the pad, x and y are relative to the top-left of the pad NOT the screen '''
    maxy, maxx = self.pad.getmaxyx()
    if len(string) > maxx:
      self.pad.addstr(y, x, string[0:maxx], attrs)
    else:
      self.pad.addstr(y, x, string, attrs)

  def refresh(self):
    self.pad.refresh(0, 0, self.pos.y, self.pos.x, self.pos.y + self.h, self.pos.x + self.w)

class UIElement(Renderable):
  def __init__(self, pos: Coordinate, w, h, visible=False):
    self.w = w
    self.h = h
    self.pos = pos
    self.visible = visible

  def toggleVisible(self):
    self.visible = not self.visible

  def render(self, gameState):
    if self.visible:
      pad = Pad(self.pos, self.w, self.h)
      #for i in range(0, self.h):
      #  pad.addstr(self.pos.y, self.pos.x, ' '*self.w)
      self.draw(pad, gameState)
      pad.refresh()

class MapViewport(UIElement):
  def __init__(self, pos, w, h):
    super().__init__(pos, w, h, visible=True)
    self.viewPos = Coordinate(0, 0)
    EventBus.registerSubscriber(EventType.MOVE_DOWN, partial(self.move, EntityAction.MOVE_DOWN.value))
    EventBus.registerSubscriber(EventType.MOVE_LEFT, partial(self.move, EntityAction.MOVE_LEFT.value))
    EventBus.registerSubscriber(EventType.MOVE_RIGHT, partial(self.move, EntityAction.MOVE_RIGHT.value))
    EventBus.registerSubscriber(EventType.MOVE_UP, partial(self.move, EntityAction.MOVE_UP.value))
    self.tileColors = {
      LAND: Color.get(curses.COLOR_BLACK, curses.COLOR_GREEN),
      WATER: Color.get(0, curses.COLOR_BLUE),
    }

  def move(self, dpos: Coordinate):
    self.viewPos += dpos

  def draw(self, pad, gameState):
    ''' Draws the map in gameState centering on the player '''
    viewPos = gameState.getPlayer().pos - Coordinate(self.w // 2, self.h // 2)
    for dy in range(self.h):
      for dx in range(self.w):
        try:
          tilePos = Coordinate(viewPos.x + dx, viewPos.y + dy)
          if tilePos.x >= 0 and tilePos.y >= 0:
            tile, entity = gameState[tilePos]
            ch = ' '
            if type(entity) == Character:
              ch = 'C'
            elif type(entity) == Player:
              ch = '@'
            elif type(entity) == NPC:
              ch = 'N'

            color = curses.color_pair(self.tileColors[gameState.map.tiles[tilePos.y][tilePos.x].name])
            pad.addstr(dy, dx, ch, color)
        except IndexError:
          pass

class StatBar(UIElement):
  def __init__(self, pos, w, h):
    super().__init__(pos, w, h, visible=True)
    self.entity = None
  
  def draw(self, pad: Pad, gameState: GameState):
    if not self.entity:
      self.entity = gameState.getPlayer()

    validActions = gameState.getValidActions(self.entity)
    pad.addstr(0, 0, str(f'{self.entity.pos} HP: {self.entity.hp}'))

    # show move actions
    keybindStr = []
    for ac in validActions:
      keybindStr.append(f'{ac.name}: {Keybindings.keyEventToKey(Keybindings.eventToKeyEvent(gameState.getPlayer().getEventFromAction(ac)))}')
    pad.addstr(1, 0, ', '.join(keybindStr))

class UI:
  def __init__(self, screen, w, h):
    self.w = w
    self.h = h
    self.scr = screen
    statBarHeight = 10
    self.uiElements = [
      MapViewport(Coordinate(0, 0), w, h - statBarHeight - 1),
      StatBar(Coordinate(0, h - statBarHeight), w, statBarHeight)
    ]
    self.initCurses()

  def initCurses(self):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.scr.keypad(True)
    self.scr.nodelay(True)

  def render(self, gameState: GameState):
    self.scr.erase()
    for uiel in self.uiElements:
      uiel.render(gameState)