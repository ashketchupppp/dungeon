import math
import random

def dictFind(dictionary, val):
  ''' Searches a dictionary for a key with value val '''
  for k in dictionary:
    if dictionary[k] == val:
      return k

possibleDirections = [
  [1, 1],
  [-1, 1],
  [1, -1],
  [-1, -1]
]
def randomDirection():
  return random.choice(possibleDirections)

class Coordinate:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  @classmethod
  def fromIterable(cls, iterable: iter):
    assert len(iterable) > 1
    return cls(iterable[0], iterable[1])

  def clamp(self):
    ''' Returns a new Coordinate whose values will always be above 0  '''
    return Coordinate(max([self.x, 0]), max([self.y, 0]))

  def __eq__(self, other):
    if type(other) == Coordinate and other.x == self.x and other.y == self.y:
      return True
    return False

  def __add__(self, other):
    if type(other) == Coordinate:
      return Coordinate(self.x + other.x, self.y + other.y)
    raise ValueError

  def __sub__(self, other):
    if type(other) == Coordinate:
      return Coordinate(self.x - other.x, self.y - other.y)
    raise ValueError
  
  def __mul__(self, other):
    if type(other) == Coordinate:
      return Coordinate(self.x * other.x, self.y * other.y)
    if type(other) == float or type(other) == int:
      return Coordinate(self.x * other, self.y * other)
    return ValueError

  def __str__(self) -> str:
      return f'{self.x},{self.y}'

  def __iter__(self):
    yield self.x
    yield self.y

  def floor(self):
    self.x = math.floor(self.x)
    self.y = math.floor(self.y)

  def dist(self, other):
    if type(other) == Coordinate:
      dist = self - other
      return math.sqrt(dist.x**2 + dist.y**2)
    raise ValueError

  def whichIsCloser(self, p1, p2):
    ''' Returns the coordinate which is closer to self '''
    if type(p1) == Coordinate and type(p2) == Coordinate:
      vecToP1 = self - p1
      distToP1 = self.dist(vecToP1)
      vecToP2 = self - p2
      distToP2 = self.dist(vecToP2)
      if distToP1 < distToP2:
        return p1
      else:
        return p2
      
    raise ValueError

def strReplace(string, replacementStr, index):
  ''' Returns the passed string with the replacement string at the given index '''
  s = list(string)
  for i in range(0, len(replacementStr)):
    try:
      s[index + i] = replacementStr[i]
    except IndexError:
      break
  return ''.join(s)

def clamp(val, max):
  ''' Clamps val to max if val is above max '''
  return val if val < max else max

def ListReplaceTwoD(l: list, listToPlace: list, x: int, y: int):
  ''' Replaces the values in list l with the values in listToPlace, starting at pos x and y at the top left '''
  # make sure we can fit listToPlace in l
  # for each line of listToPlace
    # starting at l[y + lineNo][x]
    # for each tileNo of listToPlace[lineNo]
      # check if l[y + lineNo][x + lineNo] exists
  for ltpY in range(len(listToPlace)):
    for ltpX in range(len(listToPlace[ltpY])):
      if l[y + ltpY][x + ltpX]:
        pass