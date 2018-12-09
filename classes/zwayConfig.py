class ZwayConfig:

  __hostname = "localhost";  
  __port = 8083;
  __timeout = 60;
  __username = None;
  __password = None;
  
  def __init__(self, root):
    hostname = root.find("zway/hostname");
    if (hostname != None and hostname.text.strip() != ""):
      self.setHostname(hostname.text.strip());
      
    port = root.find("zway/port");
    if (port != None and port.text.strip() != ""):
      self.setPort(int(port.text.strip()));
	  
    username = root.find("zway/username");
    if (username != None and username.text.strip() != ""):
      self.setUsername(username.text.strip());
      
    username = root.find("zway/username");
    if (username != None and username.text.strip() != ""):
      self.setUsername(username.text.strip());
      
    password = root.find("zway/password");
    if (password != None and password.text.strip() != ""):
      self.setPassword(password.text.strip());
      
  def getHostname(self):
    return self.__hostname;

  def setHostname(self, hostname):
    self.__hostname = hostname;

  def getPort(self):
    return self.__port;

  def setPort(self, port):
    self.__port = port;

  def getTimeout(self):
    return self.__timeout;

  def setTimeout(self, timeout):
    self.__timeout = timeout;
    
  def getUsername(self):
    return self.__username;
    
  def setUsername(self, username):
    self.__username = username;
    
  def getPassword(self):
    return self.__password;
    
  def setPassword(self, password):
    self.__password = password;
