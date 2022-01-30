import locale
import curses
from abc import ABC, abstractmethod

from map import LAND, WATER
from state import Character, GameState
from utils import Coordinate, strReplace, clamp
from state import Player

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
    self.tileColors = {
      LAND: Color.get(curses.COLOR_BLACK, curses.COLOR_GREEN),
      WATER: Color.get(0, curses.COLOR_BLUE),
    }

  def draw(self, pad, gameState):
    for dy in range(self.h):
      for dx in range(self.w):
        try:
          tile, entity = gameState[Coordinate(self.pos.x + dx, self.pos.y + dy)]
          ch = ' '
          if type(entity) == Character:
            ch = 'C'
          elif type(entity) == Player:
            ch = '@'

          color = curses.color_pair(self.tileColors[gameState.map.tiles[dy][dx].name])
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
    pad.addstr(0, 0, str(self.entity.pos))
    pad.addstr(1, 0, ', '.join([ac.name for ac in validActions]))

class UI:
  def __init__(self, screen, w=50, h=50):
    self.w = w
    self.h = h
    self.scr = screen
    self.uiElements = [
      MapViewport(Coordinate(0, 0), 33, 33),
      StatBar(Coordinate(0, h - 4), w, 4)
    ]
    self.initCurses()

  def initCurses(self):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.scr.keypad(True)
    self.scr.nodelay(True)

  def render(self, gameState: GameState):
    for uiel in self.uiElements:
      uiel.render(gameState)