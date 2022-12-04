import pygame
from components.Button import Button
from utils.IO import IO

class Node(Button):
  def __init__(self, x: int, y: int, mode, font: pygame.font.Font) -> None:
    self.io = IO(True)
    self.mode = mode
    self.wires = []
    super().__init__('T', x, y, 'green',font)

  def add_wire(self, w):
    self.wires.append(w)

  def getValue(self) -> bool:
    return self.io.getValue()

  def setPos(self, x: int, y: int) -> None:
    self.x = x
    self.y = y
    self.render()

  def render(self, ind = None, font = None, before = False) -> None:
    if self.io.getValue() == True and self.label == 'F':
      self.label = 'T'
      self.bg = 'green'
    elif self.io.getValue() == False and self.label == 'T':
      self.label = 'F'
      self.bg = 'red'
    return super().render(False, ind, font, before)

  def setIO(self, io: IO):
    self.io = io

  def setValue(self, value: bool) -> None:
    self.io.setValue(value)

  def onClick(self, event: pygame.event.Event) -> None:
    if self.label == 'T':
      self.label = 'F'
      self.bg = 'red'
      self.io.setValue(False)
    else:
      self.label = 'T'
      self.bg = 'green'
      self.io.setValue(True)
    
    self.render()
  