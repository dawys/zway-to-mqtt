from enum import Enum;

class Type(Enum):
	INTEGER = "INTEGER"
	LONG = "LONG"
	FLOAT = "FLOAT"
	ON_OFF = "ON_OFF"

class Topic:

	__id = None;
	__property = None;
	__type = None;
	__refreshInterval = 60;
	__invert = False;
	__path = None;

	def __init__(self, id, property, type, path, refreshInterval):
		self.setId(id);
		self.setProperty(property);
		self.setType(self.__convertType(type));
		self.setPath(path);
		self.setRefreshInterval(refreshInterval);
		self.setInvert(False);
	
	def getId(self):
		return self.__id;

	def setId(self, id):
		self.__id = id;
	
	def getProperty(self):
		return self.__property;

	def setProperty(self, property):
		self.__property = property;
	
	def getType(self):
		return self.__type;

	def setType(self, type):
		self.__type = type;
	
	def getRefreshInterval(self):
		return self.__refreshInterval;
	
	def setRefreshInterval(self, refreshInterval):
		self.__refreshInterval = refreshInterval;
	
	def getInvert(self):
		return self.__invert;

	def setInvert(self, invert):
		self.__invert = invert;
	
	def getPath(self):
		return self.__path;

	def setPath(self, path):
		self.__path = path;
	
	def __convertType(self, type):
		if (type == "INTEGER"):
			return Type.INTEGER;
		elif (type == "LONG"):
			return Type.LONG;
		elif (type == "FLOAT"):
			return Type.FLOAT;
		elif (type == "ON_OFF"):
			return Type.ON_OFF;
		return None;
	
	def log(self):
		return self.getPath() + " > " + self.getId() + "/" + self.getProperty() + " [" + self.getType() + "]";