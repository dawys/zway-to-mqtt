from enum import Enum;

class Type(Enum):
  INTEGER = 1
  FLOAT = 2
  ON_OFF = 3

class Topic:

  __id = None;
  __property = None;
  __type = None;
  __refreshinterval = 60;
  __invert = False;
  __path = None;

  def __init__(self, id, property, type, path, refreshinterval):
    self.setId(id);
    self.setProperty(property);
    self.setType(self.__convertType(type));
    self.setPath(path);
    self.setRefreshinterval(refreshinterval);
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
	
  def getRefreshinterval(self):
    return self.__refreshinterval;
	
  def setRefreshinterval(self, refreshinterval):
    self.__refreshinterval = refreshinterval;
	
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
    elif (type == "FLOAT"):
      return Type.FLOAT;
    elif (type == "ON_OFF"):
      return Type.ON_OFF;
    return None;
	
  def log(self):
    return self.getPath() + " > " + self.getId() + "/" + self.getProperty() + " [" + str(self.getType()) + "]";