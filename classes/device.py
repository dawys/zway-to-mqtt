class Device:

  __value = None;
  __updateTime = None;
  
  def __init__(self, value, updateTime):
    self.setValue(value);
    self.setUpdateTime(updateTime);
	
  def getValue(self):
    return self.__value;
	
  def setValue(self, value):
    self.__value = value;
	
  def getUpdateTime(self):
    return self.__updateTime;

  def setUpdateTime(self, updateTime):
    self.__updateTime = updateTime;