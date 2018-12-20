class Job:

	__scheduler = None;
	__nextTime = None;

	def __init__(self, scheduler, nextTime):
		self.setScheduler(scheduler);
		self.setNextTime(nextTime);

	def getScheduler(self):
		return self.__scheduler;

	def setScheduler(self, scheduler):
		self.__scheduler = scheduler;

	def getNextTime(self):
		return self.__nextTime;

	def setNextTime(self, nextTime):
		self.__nextTime = nextTime;