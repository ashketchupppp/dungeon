import curses

from eventbus import EventBus, EventType
import ui
from state import GameState

class Game:
  def __init__(self, screen):
    self.screen = screen
    self.ui = ui.UI(screen)
    self.gameState = GameState()
    self.running = False

  def quitGame(self, evt):
    self.running = False

  def step(self):
    event = self.screen.getch()
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
    
    self.gameState.step()

  def run(self):
    EventBus.registerSubscriber(EventType.KEY_Q, self.quitGame)

    self.running = True
    while self.running:
      self.ui.render(self.gameState)
      self.step()

def main(screen):
  game = Game(screen)
  game.run()

  curses.nocbreak()
  screen.keypad(False)
  curses.echo()

if __name__ == '__main__':
  curses.wrapper(main)