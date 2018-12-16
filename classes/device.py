class Device:

	__value = None;
	__force = False;
	__refreshTime = None;	
	__updateTime = None;
	
	def __init__(self, value, refreshTime, updateTime):
		self.setValue(value);
		self.setForce(False);
		self.setRefreshTime(refreshTime);	
		self.setUpdateTime(updateTime);
	
	def getValue(self):
		return self.__value;
	
	def setValue(self, value):
		self.__value = value;
	
	def getForce(self):
		return self.__force;
	
	def setForce(self, force):
		self.__force = force;
		
	def getRefreshTime(self):
		return self.__refreshTime;

	def setRefreshTime(self, refreshTime):
		self.__refreshTime = refreshTime;		
	
	def getUpdateTime(self):
		return self.__updateTime;

	def setUpdateTime(self, updateTime):
		self.__updateTime = updateTime;