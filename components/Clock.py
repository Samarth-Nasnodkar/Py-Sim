import pygame
from components.Node import Node
from utils.IO import IO
from utils.KeepRefs import KeepRefs
import math

class Clock(KeepRefs):
  def __init__(self, x: int, y: int, font, ticker = 1, fps = 1) -> None:
    super(Clock, self).__init__()
    self.x = x
    self.y = y
    self.fps = fps
    self.bg = pygame.Color('orange')
    self.ticker = ticker
    self.label = f'Clk {round(self.fps / self.ticker, 2)}'
    self.font = font
    self.height = 40
    self.cur_tik = 0
    self.is_sync = False
    self.out = IO()
    self.render()

  def setTick(self, tick: int) -> None:
    self.ticker = tick if tick > 0 else 1
    self.cur_tik = 0

  def getIO(self) -> IO:
    return self.out

  def sync(self, clk) -> None:
    self.out = clk.getIO()
    self.ticker = clk.ticker
    self.is_sync = True

  def setPos(self, x: int, y: int):
    self.x = x
    self.y = y
    self.render()

  def compute(self):
    if self.is_sync:
      return
    self.cur_tik += 1
    if self.cur_tik == self.ticker:
      self.cur_tik = 0
      self.out.toggle()

  def setOutput(self, io: IO):
    self.out = io

  def render(self) -> None:
    self.label = f'Clk {round(self.fps / self.ticker, 2)}'
    self.text = self.font.render(self.label, True, pygame.Color('black'))
    _h = self.text.get_size()[1] + 4
    self.height = 3 * _h
    self.width = 2 * self.text.get_size()[0]
    self.surface = pygame.Surface((self.width, self.height))
    self.surface.fill((128,128,128))
    pygame.draw.rect(self.surface, self.bg, (0, 0, self.width, self.height), 0, 15)
    h = _h
    n = Node(0, 0, 'output', self.font)
    n.io.setValue(self.out.getValue())
    n.render()
    self.surface.blit(n.surface, (self.width - n.textSize[0] - n.padding, h))
    self.surface.blit(self.text, (self.width // 2 - self.text.get_size()[0] // 2, self.height // 2 - 10))
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    # self.cur_tik += 1
    # if self.cur_tik == self.ticker:
    #   self.out.toggle()
    #   self.cur_tik = 0

  def isNode(self, x: int, y: int) -> bool:
    x -= self.x
    y -= self.y
    _h = self.text.get_size()[1] + 4
    dn = Node(0, 0, 'output', self.font)
    h = _h
    n = Node(self.width - dn.textSize[0] - dn.padding, h, 'output', self.font)
    if n.rect.collidepoint(x, y):
      return True
    return False