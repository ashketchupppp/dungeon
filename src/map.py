import curses
from perlin_noise import PerlinNoise

from utils import Coordinate

LAND = 'LAND'
WATER = 'WATER'
WALL = 'WALL'
FLOOR = 'FLOOR'

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

class Wall(Tile):
  def __init__(self):
    super().__init__(WALL, walkable=False)

class Floor(Tile):
  def __init__(self):
    super().__init__(FLOOR, walkable=True)

class Map:
  tileTypes = {
      LAND: Land(),
      WATER: Water(),
      WALL: Wall(),
      FLOOR: Floor()
    }

  def __init__(self, w=100, h=100, tiles=[]):
    super().__init__()
    self.map_w = w
    self.map_h = h
    self.tiles = self.generateLandmap()
    self.dimensions = (len(self.tiles), len(self.tiles[0]))

  def generateLandmap(self):
    tiles = []
    noise = PerlinNoise(octaves=2, seed=1)
    self.perlinMap = [[noise([i/self.map_w, j/self.map_h]) for j in range(self.map_w)] for i in range(self.map_h)]
    if not len(tiles):
      for i in range(self.map_h):
        tiles.append([])
        for j in range(self.map_w):
          if self.perlinMap[i][j] < 0.001:
            tiles[i].append(Map.tileTypes[WATER])
          else:
            tiles[i].append(Map.tileTypes[LAND])
    return tiles

  def toPathfindMatrix(self):
    ''' Returns self.tiles as a 2d list of 1 or 0, depending on the walkable value of the tile '''
    matrix = []
    for row in self.tiles:
      matrix.append([int(tile.walkable) for tile in row])
    return matrix

  def __getitem__(self, coord: Coordinate):
    if coord.x < 0 or coord.y < 0 or coord.y > self.map_h or coord.x > self.map_w:
      raise IndexError
    return self.tiles[coord.y][coord.x]