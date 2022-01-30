import curses
from multiprocessing import Event

from eventbus import EventBus, EventType
import ui
from state import GameState
import keybinds

class Game:
  def __init__(self, screen):
    self.screen = screen
    self.ui = ui.UI(screen)
    self.keybinds = keybinds.Keybindings()
    self.gameState = GameState()
    self.running = False

  def quitGame(self):
    self.running = False

  def run(self):
    self.keybinds.bind()
    EventBus.registerSubscriber(EventType.QUIT, self.quitGame)
    EventBus.registerSubscriber(EventType.END_TURN, self.gameState.step)

    self.running = True
    while self.running:
      self.ui.render(self.gameState)
      event = self.screen.getch()
      if event != -1:
        try:
          if event == ord('q'):
            EventBus.triggerEvent(EventType.KEY_Q)
          elif event == ord('a'):
            EventBus.triggerEvent(EventType.KEY_A)
            EventBus.triggerEvent(EventType.END_TURN)
          elif event == ord('d'):
            EventBus.triggerEvent(EventType.KEY_D)
            EventBus.triggerEvent(EventType.END_TURN)
          elif event == ord('w'):
            EventBus.triggerEvent(EventType.KEY_W)
            EventBus.triggerEvent(EventType.END_TURN)
          elif event == ord('s'):
            EventBus.triggerEvent(EventType.KEY_S)
            EventBus.triggerEvent(EventType.END_TURN)
        except EventBus.EventDoesNotExist:
          pass # we may not have all keys bound

def main(screen):
  curses.start_color()
  game = Game(screen)
  game.run()

  curses.nocbreak()
  screen.keypad(False)
  curses.echo()

if __name__ == '__main__':
  curses.wrapper(main)