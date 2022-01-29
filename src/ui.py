import locale
import curses
from abc import ABC, abstractmethod

from map import LAND, WATER
from state import GameState
from utils import strReplace

class Renderable(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def render(self, dispArea):
    raise NotImplementedError

class Color:
  colors = {}

  @classmethod
  def get(cls, fg, bg) -> int:
    if (fg, bg) in cls.colors:
      return cls.colors[(fg, bg)]
    else:
      colorNumber = len(cls.colors) + 1
      cls.colors[(fg, bg)] = colorNumber
      curses.init_pair(colorNumber, fg, bg)
      return colorNumber

class UIElement(Renderable):
  def __init__(self, x, y, w, h, visible=False):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.visible = visible

  def toggleVisible(self):
    self.visible = not self.visible

  def render(self, gameState):
    if self.visible:
      pad = curses.newpad(self.w, self.h)
      self.draw(pad, gameState)
      pad.refresh(0, 0, 0, 0, 10, 10)# self.x + self.w, self.y + self.h)

class MapViewport(UIElement):
  def __init__(self, x, y, w, h):
    super().__init__(x, y, w, h, visible=True)
    self.tileColors = {
      LAND: Color.get(0, curses.COLOR_GREEN),
      WATER: Color.get(0, curses.COLOR_BLUE),
    }

  def draw(self, pad, gameState):
    for dx in range(self.h):
      for dy in range(self.w):
        try:
          color = self.tileColors[gameState.map.tiles[dx][dy].name]
          pad.addch(dy + self.y, dx + self.x, ' ', curses.color_pair(color))
        except IndexError:
          pass

class UI:
  def __init__(self, screen, w=50, h=50):
    self.w = w
    self.h = h
    self.scr = screen
    self.uiElements = [
      MapViewport(0, 0, w, h)
    ]
    self.initCurses()

  def initCurses(self):
    locale.setlocale(locale.LC_ALL, '')
    curses.noecho()
    curses.cbreak()
    self.scr.keypad(True)
    curses.start_color()
    self.scr.nodelay(True)
    curses.curs_set(0)

  def render(self, gameState: GameState):
    for uiel in self.uiElements:
      uiel.render(gameState)

class StatBar(UIElement):
  def __init__(self, w, h, entity, visible=False):
    super().__init__(w, h, visible)
    self.entity = entity
    self.color = Color.get(curses.COLOR_WHITE, curses.COLOR_BLUE)

  def render(self, dispArea):
    if self.visible:
      num_rows, num_cols = dispArea.getmaxyx()
      y = num_rows - self.h
      x = num_cols - self.w
      stringsToDraw = [*[' '*(self.w - 1) for i in range(self.h)]]
      stringsToDraw[0] = strReplace(stringsToDraw[0], str(self.entity), 0)
      stringsToDraw[1] = strReplace(stringsToDraw[1], f'{self.entity.pos.x}, {self.entity.pos.y}', 0)

      for i in range(0, len(stringsToDraw)):
        dispArea.addstr(y + i, x, stringsToDraw[i], self.color)