from typing import List
from utils.KeepRefs import KeepRefs
import pygame
from components.Line import Line

class CircuitWire(KeepRefs):
  def __init__(self, x, y) -> None:
    super(CircuitWire, self).__init__()
    self.x = x
    self.y = y
    self.endx = x
    self.endy = y
    self.temp_wire = None
    self.wires: List[Line] = []

  def add_wire(self, wire) -> None:
    if not wire.ortho:
      self.endx, self.endy = wire._to
    else:
      d = wire.get_dir()
      if d == 'r' or d == 'l':
        self.endx = wire._to[0]
        wire._to = (wire._to[0], wire._from[1])
      else:
        self.endy = wire._to[1]
        wire._to = (wire._from[0], wire._to[1])
    self.wires.append(wire)
  
  def move_end(self, _tox, _toy):
    self.endx, self.endy = _tox, _toy
    self.wires[-1]._to = _tox, _toy

  def move_start(self, _tox, _toy):
    self.x, self.y = _tox, _toy
    self.wires[0]._from = _tox, _toy

  def draw_temp(self, _to, ortho=False):
    l = Line(self.get_end(), _to, 2, 'black', ortho)
    if not ortho:
      self.temp_wire = l
      return
    d = l.get_dir()
    if d == 'l' or d == 'r':
      l._to = (l._to[0], l._from[1])
    else:
      l._to = (l._from[0], l._to[1])
    
    self.temp_wire = l

  def get_end(self):
    return self.endx, self.endy

  def render(self, surface) -> None:
    for wire in self.wires:
      # if not wire.ortho:
      pygame.draw.line(surface, wire.color, wire._from, wire._to, wire.width)
      # else:
      #   _dir = wire.get_dir()
      #   _to = wire._to
      #   if _dir == 'l' or _dir == 'r':
      #     _to = (_to[0], wire._from[1])
      #   else:
      #     _to = (wire._from[0], _to[1])

      #   wire._to = _to
      #   pygame.draw.line(surface, wire.color, wire._from, wire._to, wire.width)

    if self.temp_wire:
      # if not self.temp_wire.ortho:
      pygame.draw.line(surface, self.temp_wire.color, self.temp_wire._from, self.temp_wire._to, self.temp_wire.width)
      # else:
      #   _dir = self.temp_wire.get_dir()
      #   _to = self.temp_wire._to
      #   if _dir == 'l' or _dir == 'r':
      #     _to = (_to[0], self.temp_wire._from[1])
      #   else:
      #     _to = (self.temp_wire._from[0], _to[1])
        
      #   pygame.draw.line(surface, self.temp_wire.color, self.temp_wire._from, _to, self.temp_wire.width)
      # pygame.draw.line(surface, 
      #                   self.temp_wire.color, 
      #                   self.temp_wire._from, 
      #                   self.temp_wire._to, 
      #                   self.temp_wire.width)
      self.temp_wire = None