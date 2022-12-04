import pygame
from components.Node import Node
from utils.KeepRefs import KeepRefs
from utils.Gate import Gate

class GateEnclosure(KeepRefs):
  def __init__(self, gate: Gate, label: str, x: int, y: int, font: pygame.font.Font):
    super(GateEnclosure, self).__init__()
    self.x = x
    self.y = y
    self.wires = []
    self.gate = gate
    self.bg = pygame.Color('orange')
    self.label = label
    self.font = font
    self.height = (2 * max(gate.inps, gate.outs) + 1) * 20
    self.render()

  def add_wire(self, w):
    self.wires.append(w)

  def setPos(self, x: int, y: int):
    self.x = x
    self.y = y
    self.render()

  def getInpIndex(self, x: int, y: int) -> int:
    x -= self.x
    y -= self.y
    _h = self.text.get_size()[1] + 4
    for i in range(self.gate.inps):
      h = (2 * i + 1) * _h
      n = Node(0, h, 'input', self.font)
      if n.rect.collidepoint(x, y):
        return i
    return -1

  def getOutIndex(self, x: int, y: int) -> int:
    x -= self.x
    y -= self.y
    _h = self.text.get_size()[1] + 4
    dn = Node(0, 0, 'output', self.font)
    for i in range(self.gate.outs):
      h = (2 * i + 1) * _h
      n = Node(self.width - dn.textSize[0] - dn.padding, h, 'output', self.font)
      if n.rect.collidepoint(x, y):
        return i
    return -1
    

  def render(self) -> None:
    self.text = self.font.render(self.label, True, pygame.Color('black'))
    _h = self.text.get_size()[1] + 4
    self.height = (2 * max(self.gate.inps, self.gate.outs) + 1) * _h
    self.width = self.text.get_size()[1] + 3 * self.text.get_size()[0]
    self.surface = pygame.Surface((self.width, self.height))
    self.surface.fill((128,128,128))
    pygame.draw.rect(self.surface, self.bg, (0, 0, self.width, self.height), 0, 15)
    for i in range(self.gate.inps):
      h = (2 * i + 1) * _h
      n = Node(0, 0, 'input', self.font)
      n.io.setValue(self.gate.inputs[i].getValue())
      n.render()
      self.surface.blit(n.surface, (0, h))
    for i in range(self.gate.outs):
      h = (2 * i + 1) * _h
      n = Node(0, 0, 'output', self.font)
      n.io.setValue(self.gate.outputs[i].getValue())
      n.render()
      self.surface.blit(n.surface, (self.width - n.textSize[0] - n.padding, h))
    
    self.surface.blit(self.text, (self.width // 2 - self.text.get_size()[0] // 2, self.height // 2 - 10))
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)