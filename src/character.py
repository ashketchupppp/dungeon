from render import Entity
from utils import Coordinate

class Character(Entity):
  def __init__(self, dispChar='C', dispAttr=0, pos = Coordinate(0, 0)):
    super().__init__(pos)
    self.dispChar = dispChar
    self.dispAttr = dispAttr

  def render(self, dispArea):
    dispArea.addstr(self.pos.y, self.pos.x, self.dispChar, self.dispAttr)

  def move(self, dpos: Coordinate):
    self.pos += dpos

class Player(Character):
  def __init__(self, pos: Coordinate):
    super().__init__(dispChar='@', pos=pos)