import unittest

from map import Tiles, TileArea

class Test_TileArea(unittest.TestCase):
  def test_place(self):
    a = TileArea(100, 100, Tiles.WALL)
    r = TileArea(10, 10, Tiles.FLOOR)
    a.place(r, 0, 0)
    for y in range(10):
      for x in range(10):
        self.assertEqual(Tiles.get(Tiles.FLOOR), a.tiles[y][x])

if __name__ == '__main__':
  unittest.main()