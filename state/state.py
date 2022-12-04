from components.GateEnclosure import GateEnclosure

class State:
  def __init__(self, name, gates, inps: list, outs: list) -> None:
    self.name = name
    self.gates = gates
    self.inps = inps
    self.outs = outs
    self.data = [[False] * len(outs)] * (2 ** len(inps))
    self._map()

  def _map(self):
    l = len(self.inps)
    for i in range(2 ** l):
      d = format(i, 'b')
      d = d[::-1]
      vals = [False] * l
      outs = [False] * len(self.outs)
      for j in range(len(d)):
        vals[l - j - 1] = d[j] == '1'
      
      for ind, inp in enumerate(self.inps):
        inp.setValue(vals[ind])

      for gate in self.gates:
        gate.gate.compute()

      for ind, out in enumerate(self.outs):
        outs[ind] = out.getValue()

      print(vals, outs)

      self.data[i] = outs

  def __dict__(self):
    return {
      'name': self.name,
      'outputs': self.data
    }