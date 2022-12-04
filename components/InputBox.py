import pygame

class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
      self.rect = pygame.Rect(x, y, w, h)
      self.color = 'white'
      self.text = text
      self.font = font
      self.done_func = None
      self.doneTyping = False
      self.txt_surface = self.font.render(text, True, self.color)
      self.active = False

    def when_done_typing(self, func = None, *args, **kwargs):
      def done_func():
        func(*args, **kwargs)

      self.done_func = done_func

    def handle_event(self, event):
      if event.key == pygame.K_RETURN:
        self.doneTyping = True
        self.active = False
        if self.done_func:
          self.done_func()
      elif event.key == pygame.K_BACKSPACE:
        self.text = self.text[:-1]
      else:
        if len(self.text) < 10:
          self.text += event.unicode
      # Re-render the text.
      self.txt_surface = self.font.render(self.text, True, 'black')

    def update(self):
      # Resize the box if the text is too long.
      width = max(200, self.txt_surface.get_width()+10)
      self.rect.w = width

    def render(self, screen):
      if not self.active:
        return
      
      # Blit the rect.
      pygame.draw.rect(screen, 'white', self.rect)
      pygame.draw.rect(screen, 'black', self.rect, 2)
      # Blit the text.
      screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
