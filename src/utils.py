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

  def __str__(self) -> str:
      return f'{self.x},{self.y}'

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

