import logging;
import sys;

class LoggingConfig:
  
  __level = "DEBUG";
  __format = "%(asctime)-15s %(message)s";
  __filePath = "/var/log/logger.log";

  def __init__(self, root):
    level = root.find("logger/level");
    if (level != None and level.text.strip() != ""):
      self.__setLevel(level.text.strip());
	  
    format= root.find("logger/format");
    if (format != None and format.text.strip() != ""):
      self.__setFormat(format.text.strip());
	  
    filePath = root.find("logger/filePath");
    if (filePath != None and filePath.text.strip() != ""):
      self.__setFilePath(filePath.text.strip());
	  
    level = None;
    if (self.__getLevel() == "INFO"):
      level = logging.INFO;
    elif (self.__getLevel() == "WARNING"):
      level = logging.WARNING;	
    elif (self.__getLevel() == "ERROR"):
      level = logging.ERROR;
    else:
      level = logging.DEBUG;
	  
    formatter = logging.Formatter(self.__getFormat());
	  
    root = logging.getLogger();
    root.setLevel(level)
	
    stdoutHandler = logging.StreamHandler(sys.stdout);
    stdoutHandler.setLevel(level);
    stdoutHandler.setFormatter(formatter)
    root.addHandler(stdoutHandler);
	
    fileHandler = logging.FileHandler(filename = self.__getFilePath());
    fileHandler.setLevel(logging.DEBUG);
    fileHandler.setFormatter(formatter)
    root.addHandler(fileHandler);
	
    if (level == logging.INFO):
      logging.info("Loglevel: INFO");	
    elif (level == logging.WARNING):
      logging.info("Loglevel: WARNING");	
    elif (level == logging.ERROR):
      logging.info("Loglevel: ERROR");
    else:
      logging.info("Loglevel: DEBUG");
	  
  def __getLevel(self):
    return self.__level;
    
  def __setLevel(self, level):
    self.__level = level;	
	
  def __getFormat(self):
    return self.__format;
    
  def __setFormat(self, format):
    self.__format = format;	
	
  def __getFilePath(self):
    return self.__filePath;
    
  def __setFilePath(self, filePath):
    self.__filePath = filePath;	