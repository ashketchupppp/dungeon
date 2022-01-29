import locale
import curses
from abc import ABC, abstractmethod
from multiprocessing import Event

from eventbus import EventBus
from utils import Coordinate

class Renderable(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def render(self, dispArea):
    raise NotImplementedError

class Entity(Renderable):
  def __init__(self, pos: Coordinate):
    self.pos = pos

class Color:
  colors = []

  @classmethod
  def add(cls, fg, bg) -> int:
    cls.colors.append((fg, bg))
    curses.init_pair(len(cls.colors), fg, bg)
    return len(cls.colors) 

class Renderer:
  def __init__(self, screen, w=50, h=50):
    self.w = w
    self.h = h
    self.scr = screen
    locale.setlocale(locale.LC_ALL, '')
    curses.noecho()
    curses.cbreak()
    self.scr.keypad(True)
    curses.start_color()
    self.scr.nodelay(True)
    curses.curs_set(0)

  def getEvents(self):
    return self.scr.getch()

  def render(self, renderables: list):
    pad_w, pad_h = curses.COLS * 2, curses.LINES * 2
    pad = curses.newpad(pad_w, pad_h)

    # draw from the top left of the pad at 0, 0
    padsection_x0, padsection_x1 = 0, 0

    # draw the pad onto the screen starting from 0, 0 to the width and height of the screen
    win_x0, win_y0, win_x1, win_y1 = 0, 0, curses.COLS - 1, curses.LINES - 1
    
    for renderable in renderables:
        renderable.render(pad)

    pad.refresh(padsection_x0, padsection_x1, win_x0, win_y0, 1, 1)