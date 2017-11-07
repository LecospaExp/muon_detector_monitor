import serial
import time
import matplotlib.pyplot as plt
import random
from threading import Timer
import threading
import numpy as np


# parameter
binRange = [0, 50]
period = 5
desc = 'th_0.3v'

def parseInt(x):
	try:
		return int(x)
	except ValueError:
		return None;
def write2file(str):
	print str
	file = open("data.txt", "w");
	file.write(str+'\n');
	file.close();

SerCounter = serial.Serial('/dev/ttyUSB0',115200)
SerCounter.flushInput()
counterArr = [ [] for _ in range(9)]
counter = [ 0 for _ in range(9)]


fig, axarr = plt.subplots(3, 3, figsize=(15,9))
axarr = axarr.ravel()

event = threading.Event()

def countThread():
	global counter, SerCounter
	while True:
		inputD = SerCounter.read()
		newEvtCh = parseInt(inputD);
		if newEvtCh is not None and newEvtCh-1 in range(9):
			counter[newEvtCh-1]+=1
def countdownThread():
	global event, period
	while True:
		time.sleep(period)
		event.set()

t1 = Timer(0, countdownThread)	
t1.start()
t = Timer(0, countThread)	
t.start()

strTime = time.time()
while True:
	event.clear()
	event.wait()
	plt.suptitle('Total time:'+str(time.time()-strTime))
	# print counter
	
	for idx, ax in enumerate(axarr):
		counterArr[idx]+=[counter[idx]]


		ax.clear()
		ax.set_title('CH_'+str(idx+1))
		if idx/3==2:
			ax.set_xlabel("# of hit in "+str(period)+" sec")
		if idx%3==0:
			ax.set_ylabel("Count")
		entries, bin_edges, patches  = ax.hist(counterArr[idx], range=binRange, bins=binRange[1], normed=True)

		numHit = np.array(counterArr[idx], dtype=np.float64)
		text  = "Total "+str(np.sum(numHit))+"\n"
		text += "Mean  "+str(np.round(np.mean(numHit),4))+"\n"
		text += "Var   "+str(np.round(np.var(numHit),4))+"\n"
		text += "Rate  "+str(np.round(np.var(numHit)/5,4))+"\n"

		ax.text(ax.get_xlim()[1]-20, ax.get_ylim()[1]/2, text,family="monospace",
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

	counter = [0 for _ in range(9)]



	plt.draw()
	plt.pause(0.01)
	plt.savefig('noh_'+str(period)+'_s_'+desc+'.jpg')
	
SerCounter.close()