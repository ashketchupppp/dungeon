import curses
from perlin_noise import PerlinNoise

from utils import Coordinate

LAND = 'LAND'
WATER = 'WATER'

class Tile:
  def __init__(self, name, walkable = True):
    self.name = name
    self.walkable = walkable

class Land(Tile):
  def __init__(self):
    super().__init__(LAND, walkable=True)

class Water(Tile):
  def __init__(self):
    super().__init__(WATER, walkable=False)

class Map:
  tileTypes = {
      LAND: Land(),
      WATER: Water()
    }

  def __init__(self, w=33, h=33, tiles=[]):
    super().__init__()
    self.map_w = w
    self.map_h = h
    noise = PerlinNoise(octaves=2, seed=1)
    self.perlinMap = [[noise([i/self.map_w, j/self.map_h]) for j in range(self.map_w)] for i in range(self.map_h)]
    self.tiles = tiles
    if not len(tiles):
      for i in range(self.map_h):
        self.tiles.append([])
        for j in range(self.map_w):
          if self.perlinMap[i][j] < 0.001:
            self.tiles[i].append(Map.tileTypes[WATER])
          else:
            self.tiles[i].append(Map.tileTypes[LAND])
    self.dimensions = (len(self.tiles), len(self.tiles[0]))

  def __getitem__(self, coord: Coordinate):
    if coord.x < 0 or coord.y < 0 or coord.y > self.map_h or coord.x > self.map_w:
      raise IndexError
    return self.tiles[coord.x][coord.y]