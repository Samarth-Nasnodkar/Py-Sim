from utils.Wire import Wire
from typing import List

class Gate:
  def __init__(self, inputs: List[Wire], outputs: List[Wire]) -> None:
    self.inputs = inputs
    self.outputs = outputs
    self.inps = len(inputs)
    self.outs = len(outputs)

  def setInput(self, index: int, inp: Wire) -> None:
    self.inputs.__setitem__(index, inp)

  def setOutput(self, index: int, out: Wire) -> None:
    self.outputs.__setitem__(index, out)

  def compute(self) -> None:
    pass