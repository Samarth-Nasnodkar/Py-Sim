from typing import List
from utils.Gate import Gate
from utils.Wire import Wire
import json

class StateGate(Gate):
  def __init__(self, name, inputs: List[Wire], outputs: List[Wire]) -> None:
    self.name = name
    self.state = {}
    self.load()
    super().__init__(inputs, outputs)

  def load(self):
    with open('state/storage.json', 'r') as f:
      states = json.load(f)
    
    for state in states:
      if state['name'] == self.name:
        self.state = state

  def compute(self):
    _bin = ''.join(['1' if inp.getValue() else '0' for inp in self.inputs])
    ind = int(_bin, 2)
    outputs = self.state['outputs'][ind]
    for i, out in enumerate(self.outputs):
      out.setValue(outputs[i])