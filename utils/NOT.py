from utils.Gate import Gate
from utils.Wire import Wire

class NOT(Gate):
  def __init__(self, input1, output) -> None:
    super().__init__([input1], [output])
    self.compute()

  def compute(self) -> None:
    val = self.inputs[0].getValue()
    self.outputs[0].setValue(not val)

  def compute_val(self, inps) -> bool:
    return not inps[0]