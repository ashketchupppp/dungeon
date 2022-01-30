import math

def dictFind(dictionary, val):
  ''' Searches a dictionary for a key with value val '''
  for k in dictionary:
    if dictionary[k] == val:
      return k

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

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

  def __str__(self) -> str:
      return f'{self.x},{self.y}'

  def __iter__(self):
    yield self.x
    yield self.y

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