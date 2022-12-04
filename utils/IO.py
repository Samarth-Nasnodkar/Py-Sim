class IO:
  def __init__(self, value: bool = True) -> None:
    self.__value = value

  def getValue(self) -> bool:
    return self.__value

  def setValue(self, value: bool) -> None:
    self.__value = value

  def toggle(self) -> None:
    self.__value = not self.__value