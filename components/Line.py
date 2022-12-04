class Line:
  def __init__(self, _from: tuple, _to: tuple, width: float, color, ortho=False) -> None:
    self._from = _from
    self._to = _to
    self.width = width
    self.color = color
    self.ortho = ortho

  def get_dir(self):
    dx = self._to[0] - self._from[0]
    dy = self._to[1] - self._from[1]
    if dx == 0:
      if dy > 0:
        return 'b'
      else:
        return 't'
    
    slope = dy / dx
    if dx > 0:
      if slope >= 1:
        return 'b'
      elif slope <= -1:
        return 't'
      else:
        return 'r'
    else:
      if slope <= -1:
        return 'b'
      elif slope >= 1:
        return 't'
      else:
        return 'l' 