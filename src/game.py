import curses
import enum
from abc import ABC, abstractmethod
from tkinter import EventType

import character
from eventbus import EventBus, EventType
import render
import map as _map
from ui import StatBar
from utils import Coordinate

class Game:
  def __init__(self, screen):
    self.screen = render.Renderer(screen)
    self.map = _map.Map()
    self.player = character.Player(Coordinate(0, 0))
    self.uiElements = [
      StatBar(self.screen.w, 3, self.player, visible=True)
    ]
    self.entities = [
      self.player,
      character.Character(pos=Coordinate(x=10, y=10))
    ]
    self.running = False

  def registerEventSubscribers(self):
    EventBus.registerSubscriber(EventType.KEY_Q, self.quitGame)
    EventBus.registerSubscriber(EventType.KEY_D, self.movePlayer)
    EventBus.registerSubscriber(EventType.KEY_A, self.movePlayer)
    EventBus.registerSubscriber(EventType.KEY_S, self.movePlayer)
    EventBus.registerSubscriber(EventType.KEY_W, self.movePlayer)

  def quitGame(self, evt):
    self.running = False

  def movePlayer(self, evt):
    dpos = Coordinate(0, 0)
    if evt == EventType.KEY_W:
      dpos = Coordinate(0, -1)
    elif evt == EventType.KEY_S:
      dpos = Coordinate(0, 1)
    elif evt == EventType.KEY_A:
      dpos = Coordinate(-1, 0)
    elif evt == EventType.KEY_D:
      dpos = Coordinate(1, 0)

    canMoveToPos = self.entityCanMoveToPos(self.player.pos + dpos)
    if canMoveToPos:
      self.player.move(dpos)

  def entityCanMoveToPos(self, pos: Coordinate):
    targetTile = self.getTileAtPos(pos)
    entityAtPos = self.getEntityAtPos(pos)
  
    if not targetTile: # trying to move out of bounds
      return False
    elif not targetTile.walkable:
      return False

    if entityAtPos: # already an entity in that tile
      return False
    
    return True

  def getEntityAtPos(self, pos: Coordinate):
    ''' Returns an entity at pos, if there is one '''
    for i in self.entities:
      if i.pos == pos:
        return i

  def getTileAtPos(self, pos: Coordinate):
    ''' Returns the tiletype at pos '''
    try:
      return self.map[pos]
    except IndexError:
      pass

  def step(self):
    event = self.screen.getEvents()

    if event != -1:
      try:
        if event == ord('q'):
          EventBus.triggerEvent(EventType.KEY_Q)
        elif event == ord('a'):
          EventBus.triggerEvent(EventType.KEY_A)
        elif event == ord('d'):
          EventBus.triggerEvent(EventType.KEY_D)
        elif event == ord('w'):
          EventBus.triggerEvent(EventType.KEY_W)
        elif event == ord('s'):
          EventBus.triggerEvent(EventType.KEY_S)
      except EventBus.EventDoesNotExist:
        pass # we may not have all keys bound

  def run(self):
    self.registerEventSubscribers()
    self.running = True
    while self.running:
      self.render()
      self.step()

  def render(self):
    self.screen.render([
      self.map,
      *self.entities,
      *self.uiElements
    ])

def main(screen):
  game = Game(screen)
  game.run()

  curses.nocbreak()
  screen.keypad(False)
  curses.echo()

if __name__ == '__main__':
  curses.wrapper(main)