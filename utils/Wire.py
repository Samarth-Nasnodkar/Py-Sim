from utils.IO import IO

class Wire:
  def __init__(self, io: IO) -> None:
    self.__io = io

  def getValue(self) -> bool:
    return self.__io.getValue()

  def setValue(self, value: bool) -> None:
    self.__io.setValue(value)

  def getIO(self) -> IO:
    return self.__io

  def setIO(self, io: IO) -> None:
    self.io = io