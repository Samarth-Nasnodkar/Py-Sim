import pygame
from utils.KeepRefs import KeepRefs

class Button(KeepRefs):
  def __init__(self, text: str, x: int, y: int, bg: pygame.Color,font: pygame.font.Font) -> None:
    super(Button, self).__init__()
    self.x = x
    self.y = y
    self.label = text
    self.font = font
    self.bg = bg
    self.padding = 8
    self.render()
    
  def render(self, keep_dims = False, _lbl = None, font_small = None, before = False) -> None:
    if _lbl is None:
      self.text = self.font.render(self.label, True, pygame.Color('black'))
      if not keep_dims:
        self.textSize = self.text.get_size()
      self.height = self.textSize[1] + self.padding
      self.width = self.textSize[0] + self.padding
      self.surface = pygame.Surface((self.width, self.height))
      self.surface.fill(self.bg)
      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
      pygame.draw.rect(self.surface, 'black', (0, 0, self.width, self.height), 2)
      self.surface.blit(self.text, (self.padding // 2, self.padding // 2))
    else:
      self.text = self.font.render(self.label, True, pygame.Color('black'))
      lblText = font_small.render(str(_lbl), True, pygame.Color('black'))
      lbl_width, lbl_height = lblText.get_size()
      if not keep_dims:
        self.textSize = self.text.get_size()
      self.height = self.textSize[1] + self.padding
      self.width = self.textSize[0] + self.padding
      _h = (self.height - lbl_height) // 2
      self.surface = pygame.Surface((self.width + lbl_width, self.height))
      self.surface.fill((128,128,128))
      if not before:
        pygame.draw.rect(self.surface, self.bg, (0, 0, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, 'black', (0, 0, self.width, self.height), 2)
        self.surface.blit(self.text, (self.padding // 2, self.padding // 2))
        pygame.draw.rect(self.surface, 'white', (self.width, _h, lbl_width, lbl_height))
        self.surface.blit(lblText, (self.width, _h))
      else:
        pygame.draw.rect(self.surface, self.bg, (lbl_width, 0, self.width, self.height))
        self.rect = pygame.Rect(self.x + lbl_width, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, 'black', (lbl_width, 0, self.width, self.height), 2)
        self.surface.blit(self.text, (lbl_width + self.padding // 2, self.padding // 2))
        pygame.draw.rect(self.surface, 'white', (0, _h, lbl_width, lbl_height))
        self.surface.blit(lblText, (0, _h))

  def setBackground(self, color: pygame.Color) -> None:
    self.bg = color
    self.render()

  def setLabel(self, text: str, keep_dims = False) -> None:
    self.label = text
    self.render(keep_dims=keep_dims)

  def onClick(self, event: pygame.event.Event) -> None:
    pass