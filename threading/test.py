import multiprocessing
from multiprocessing.managers import BaseManager
from time import sleep,time

class yote:
	def __init__(self,data=None):
		self.data = data
		self.k = 1
		self.p = 2
		
	def getK(self): return self.k
	def getP(self): return self.p
	def setK(self,d): self.k = d
	def setP(self,p): self.p = d
	
class fuck:
	def __init__(self):
		print("fuck")
	
	def run(self,d):
		while(1):
			print("fuck",d.getK(),d.getP())
			d.setK(d.getK() + 1)

class fook:
	def __init__(self):
		print("fook")

	def run(self,d):
		while(1):
			print("fook",d.getK(),d.getP())
			d.setK(d.getK() + 1)
	
if __name__ == "__main__":
	
	f = fuck()
	fo = fook()

	BaseManager.register("myData",yote)
	m = BaseManager()
	m.start()
	
	y = m.myData(0)
	x = m.Data2(0)
	
	p1 = multiprocessing.Process(target = f.run, args=(y,))
	p2 = multiprocessing.Process(target = fo.run,args=(y,))

	p1.start()
	p2.start()
	while(1):
		continue
