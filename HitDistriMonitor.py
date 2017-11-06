import serial
import time
import matplotlib.pyplot as plt
import random
from threading import Timer
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
counter = [0]*9
strTime = round(time.time(),5);


while True:
	loop = 0
	while loop<10:

		inputD = SerCounter.read()
		# inputD = random.sample(range(1,10),1)[0]

		newEvtCh = parseInt(inputD);
		if newEvtCh is not None and newEvtCh>0 and newEvtCh<9:
			loop+=1
			counter[newEvtCh-1]+=1
	plt.bar(range(1, 10), counter, align='center')
	plt.draw()
	plt.pause(0.01)
	write2file(', '.join(map(str, [round(time.time(),5)-strTime]+counter)))		
SerCounter.close()