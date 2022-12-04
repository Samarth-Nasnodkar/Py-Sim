import json

from state.state import State

class StateSaver:
  def __init__(self) -> None:
    self.data = []
    self.loaded = False
    self.load()

  def load(self):
    with open('state/storage.json', 'r') as f:
      self.data = json.load(f)
    
    self.loaded = True

  def save(self, state: State):
    self.data.append(state.__dict__())
    with open('state/storage.json', 'w') as f:
      json.dump(self.data, f)

    self.loaded = True