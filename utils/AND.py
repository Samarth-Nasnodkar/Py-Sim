from utils.Gate import Gate
from utils.Wire import Wire

class AND(Gate):
  def __init__(self, input1, input2, output) -> None:
    super().__init__([input1, input2], [output])
    self.compute()

  def compute(self) -> None:
    val = True
    for _inp in self.inputs:
      val = val and _inp.getValue()
    
    self.outputs[0].setValue(val)

  def compute_val(self, inps) -> bool:
    val = True
    for inp in inps:
      val = val and inp
    
    return val