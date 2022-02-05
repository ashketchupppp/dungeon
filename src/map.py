import unittest
from perlin_noise import PerlinNoise
import numpy as np
import networkx as nx
import random

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
    self.clear(tType)

  def __getitem__(self, i):
    return self.tiles[i]

  def __len__(self):
    return len(self.tiles)

  def clear(self, tType: int):
    ''' Changes all tiles to be tType '''
    self.tiles = np.array([[tType for t in range(self.w)] for x in range(self.h)])

  def placeArea(self, area, x: int, y: int):
    ''' Places tiles from area into tiles of another area at position x, y
        https://numpy.org/doc/stable/user/basics.indexing.html "Dimensional indexing tools"
    '''
    self.tiles[y:area.tiles.shape[0] + y, x:area.tiles.shape[1] + x] = area.tiles

class Rooms:
  def __init__(self, n: int, maxW: int, maxH: int, minW: int, minH: int):
    self.graph = nx.minimum_spanning_tree(nx.random_regular_graph(n // 3, n))
    for node in self.graph.nodes:
      self.graph.nodes[node]['area'] = TileArea(
        random.randint(minW, maxW),
        random.randint(minH, maxH),
        tType=Tiles.FLOOR
      )
    for edge in self.graph.edges:
      self.graph.edges[edge]['dist'] = random.randint()

  def nodes(self, data=False) -> list:
    ''' If data is false then returns a list of graph nodes, list(int)
        If data is true then returns a list of tuples, list(tuple(int, dict)) where dict is the node data
    '''
    return self.graph.nodes.data(data=data)

class Map(TileArea):
  def __init__(self, w=100, h=100, tType=Tiles.WATER):
    super().__init__(w, h, tType)
    self.defaultTile = tType
    self.generateDungeon(2)

  def generateLandmap(self):
    self.clear(self.defaultTile)
    noise = PerlinNoise(octaves=2, seed=1)
    perlinMap = [[noise([i/self.w, j/self.h]) for j in range(self.w)] for i in range(self.h)]
    for j in range(self.h):
      for i in range(self.w):
        if perlinMap[j][i] > 0.001:
          self.tiles[j][i] = Tiles.LAND

  def generateDungeon(self, numRooms: int, maxW=10, maxH=10, minW=2, minH=2):
    self.clear(Tiles.WALL)
    rooms = Rooms(numRooms, maxW, maxH, minW, minH)
    for room in rooms.nodes(data=True):
      self.placeArea(room[1]['area'], 5, 5)

  def toWalkable(self):
    ''' Returns self.tiles as a 2d list of 1 or 0, depending on the walkable value of the tile '''
    def mapping(t):
      return int(Tiles.get(t).walkable)
    return np.vectorize(mapping)(self.tiles)

  def __getitem__(self, coord: Coordinate):
    if coord.x < 0 or coord.y < 0 or coord.y > self.h or coord.x > self.w:
      raise IndexError
    return self.tiles[coord.y][coord.x]