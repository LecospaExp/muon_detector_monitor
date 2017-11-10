import serial
import time
import matplotlib.pyplot as plt
import random
from threading import Timer
import threading
import numpy as np


# parameter
Vth 	= 10 	#mv
ChNum 	= 1 	# channel number
stopTh 	= 5 #hit
period 	= 5 	#s

# plot params
binRange = [0, 30]

def parseInt(x):
	try:
		return int(x)
	except ValueError:
		return None;
def write2file(str):
	print str
	file = open("data.txt", "a");
	file.write(str+'\n');
	file.close();

SerCounter = serial.Serial('/dev/ttyAMA0',115200)
SerCounter.flushInput()
counterArr = []
counter = 0


fig = plt.figure(figsize=(8,6))

event = threading.Event()
keep = True
def countThread():
	global counter, SerCounter, keep
	while keep:
		inputD = SerCounter.read()
		newEvtCh = parseInt(inputD);
		if newEvtCh is ChNum:
			counter += 1
			print newEvtCh
	SerCounter.close()
def countdownThread():
	global event, period, keep
	while keep:
		time.sleep(period-0.005)
		event.set()

t1 = Timer(0, countdownThread)	
t = Timer(0, countThread)	

strTime = time.time()
totaltime = 0
totalhit  = 0
totalIter = 0
totalMean = 0
totalVar  = 0
avgRate   = 0

t.start()
t1.start()
counter = 0

while True:
	totalIter += 1
	event.clear()
	event.wait()
	plt.clf()

		
	totaltime = time.time()-strTime
	counterArr+=[counter]
	counter = 0
	plt.suptitle('Total iter:'+str(totalIter)+' Total time:'+str(np.round(time.time()-strTime, 3))+ 's')
	plt.title('CH_'+str(ChNum))
	plt.xlabel("# of hit in "+str(period)+" sec")
	plt.ylabel("Count")

	entries, bin_edges, patches  = plt.hist(counterArr, range=binRange, bins=binRange[1], normed=True)

	numHit = np.array(counterArr, dtype=np.float64)
	totalhit, totalMean, totalVar = np.sum(numHit), np.round(np.mean(numHit),4), np.round(np.var(numHit),4)
	avgRate = np.round(totalhit/totaltime,4)
	text  = "Total "+str(totalhit)+"\n"
	text += "Mean  "+str(totalMean)+"\n"
	text += "Var   "+str(totalVar)+"\n"
	text += "Rate  "+str(avgRate)+"\n"

	plt.text(plt.gca().get_xlim()[1]-6, plt.gca().get_ylim()[1]/2, text,family="monospace",
    bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

	


	plt.draw()
	plt.pause(0.00000001)
	plt.savefig('noh_'+str(period)+'_s_CH'+str(ChNum)+'_Vth-'+str(Vth)+'mv.jpg')
	if(np.sum(numHit)>stopTh):
		keep = False
		break
write2file(",".join(map(str, [Vth, avgRate, totalhit, totaltime, totalIter, totalMean, totalVar])))