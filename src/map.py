import curses
from perlin_noise import PerlinNoise

from render import Renderable, Color
from constants import X, Y
from utils import Coordinate
from ui import UIElement

Land = 'Land'
WATER = 'WATER'

class Tile:
  def __init__(self, name, bgColor, walkable = True):
    self.name = name
    self.bgColor = bgColor
    self.color = Color.add(0, self.bgColor)
    self.walkable = walkable

  def render(self, dispArea, x, y):
    dispArea.addstr(y, x, ' ', curses.color_pair(self.color))

class Land(Tile):
  def __init__(self):
    super().__init__('Land', curses.COLOR_GREEN, walkable=True)

class Water(Tile):
  def __init__(self):
    super().__init__('Water', curses.COLOR_BLUE, walkable=False)

class Map(Renderable):
  def __init__(self, x=0, y=0, w=33, h=33, tiles=[]):
    super().__init__()
    self.x = x
    self.y = y
    self.map_w = w
    self.map_h = h
    self.tileTypes = {
      'LAND': Land(),
      'WATER': Water()
    }
    noise = PerlinNoise(octaves=2, seed=1)
    self.perlinMap = [[noise([i/self.map_w, j/self.map_h]) for j in range(self.map_w)] for i in range(self.map_h)]
    self.tiles = tiles
    if not len(tiles):
      for i in range(self.map_h):
        self.tiles.append([])
        for j in range(self.map_w):
          if self.perlinMap[i][j] < 0.001:
            self.tiles[i].append(self.tileTypes['WATER'])
          else:
            self.tiles[i].append(self.tileTypes['LAND'])
    self.dimensions = (len(self.tiles), len(self.tiles[0]))

  def __getitem__(self, coord: Coordinate):
    if coord.x < 0 or coord.y < 0 or coord.y > self.map_h or coord.x > self.map_w:
      raise IndexError
    return self.tiles[coord.x][coord.y]

  def render(self, pad):
    for dx in range(self.dimensions[X]):
      for dy in range(self.dimensions[Y]):
        pad.addstr(dy + self.y, dx + self.x, ' ', curses.color_pair(self.tiles[dx][dy].color))