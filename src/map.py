import unittest
from perlin_noise import PerlinNoise
import numpy as np

from utils import Coordinate

class Tile:
  def __init__(self, name, walkable = True):
    self.name = name
    self.walkable = walkable

  def __getitem__(self, i):
    return 

class Land(Tile):
  def __init__(self):
    super().__init__(type(self).__name__, walkable=True)

class Water(Tile):
  def __init__(self):
    super().__init__(type(self).__name__, walkable=False)

class Wall(Tile):
  def __init__(self):
    super().__init__(type(self).__name__, walkable=False)

class Floor(Tile):
  def __init__(self):
    super().__init__(type(self).__name__, walkable=True)

class Tiles:
  '''  Class for storing the available tiles '''
  LAND = 0
  WATER = 1
  WALL = 2
  FLOOR = 3

  _TILES = [
    Land(),
    Water(),
    Wall(),
    Floor()
  ]

  @classmethod
  def get(cls, i):
    return cls._TILES[i]

class TileArea:
  ''' Stores a rectangular area of tiles with width w and height h '''
  def __init__(self, w, h, tType=Tiles.WATER):
    self.w = w
    self.h = h
    self.tiles = np.array([[tType for t in range(w)] for x in range(h)])

  def __getitem__(self, i):
    return self.tiles[i]

  def __len__(self):
    return len(self.tiles)

  def placeArea(self, area, x: int, y: int):
    ''' Places tiles from area into tiles of another area at position x, y
        https://numpy.org/doc/stable/user/basics.indexing.html "Dimensional indexing tools"
    '''
    self.tiles[y:area.tiles.shape[0] + y, x:area.tiles.shape[1] + x] = area.tiles

class Map:
  def __init__(self, w=100, h=100, tiles=[]):
    super().__init__()
    self.map_w = w
    self.map_h = h
    self.tiles = self.generateLandmap()
    self.dimensions = (len(self.tiles), len(self.tiles[0]))

  def generateLandmap(self):
    tiles = TileArea(self.map_w, self.map_h)
    noise = PerlinNoise(octaves=2, seed=1)
    perlinMap = [[noise([i/self.map_w, j/self.map_h]) for j in range(self.map_w)] for i in range(self.map_h)]
    for j in range(self.map_h):
      for i in range(self.map_w):
        if perlinMap[j][i] > 0.001:
          tiles[j][i] = Tiles.LAND
    return tiles

  def toPathfindMatrix(self):
    ''' Returns self.tiles as a 2d list of 1 or 0, depending on the walkable value of the tile '''
    def mapping(t):
      return int(Tiles.get(t).walkable)
    return np.vectorize(mapping)(self.tiles)

  def __getitem__(self, coord: Coordinate):
    if coord.x < 0 or coord.y < 0 or coord.y > self.map_h or coord.x > self.map_w:
      raise IndexError
    return self.tiles[coord.y][coord.x]