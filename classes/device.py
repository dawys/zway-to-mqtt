class Device:

  __value = None;
  __force = False;
  __updateTime = None;
  
  def __init__(self, value, updateTime):
    self.setValue(value);
    self.setForce(False);
    self.setUpdateTime(updateTime);
	
  def getValue(self):
    return self.__value;
	
  def setValue(self, value):
    self.__value = value;
	
  def getForce(self):
    return self.__force;
	
  def setForce(self, force):
    self.__force = force;
	
  def getUpdateTime(self):
    return self.__updateTime;

  def setUpdateTime(self, updateTime):
    self.__updateTime = updateTime;