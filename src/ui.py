import curses

from render import Renderable, Color
from utils import strReplace

class UIElement(Renderable):
  def __init__(self, w, h, visible=False):
    self.w = w
    self.h = h
    self.visible = visible

  def toggleVisible(self):
    self.visible = not self.visible

  def render(self):
    raise NotImplementedError

class StatBar(UIElement):
  def __init__(self, w, h, entity, visible=False):
    super().__init__(w, h, visible)
    self.entity = entity
    self.color = Color.add(curses.COLOR_WHITE, curses.COLOR_BLUE)

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