import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import RPi.GPIO as GPIO

# Change string to integer
def parseInt(x):
	try:
		return int(x);
	except ValueError:
		return None;

# Write data to txt file
def write2file(string):
	file = open("data.txt", "a");
	file.write(string+'\n');
	print string;
	file.close();

# Reset trigger
GPIO.setup(16, GPIO.IN);

start_time = round(time.time(), 5);

input_data = serial.Serial('/dev/ttyUSB0',115200);
bins = [1,2,3,4,5,6,7,8,9]
counter = [0]*9;
muon = [];


write2file('===Start counting from '+str(start_time)+'===');

plt.ion();

if GPIO.input(16):
    counter = [0]*9;
else:
# while True:
	event = parseInt(input_data.readline());
	print(event);

	if event!=None and event>=1 and event<=9:
		# Write into file.
		counter[event-1] += 1;
		muon += [event];
		# print muon;
		current_time = round(time.time(),5);
		
		write2file(str(current_time)+','+str(counter));
		
		# Plot histogram.

		fig_name = "./bar/fig_" + str(len(muon));

		plt.cla();
		
		# plt.hist(muon,bins);
		plt.title("Histogram");
		plt.xlabel("No.");
		plt.ylabel("Count");

		objects = ('1','2','3','4','5','6','7','8','9');
		y_pos = np.arange(len(objects));
		# performance = [10,8,6,4,2,1];
		 
		plt.bar(y_pos, counter, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		# plt.ylabel('Usage')
		# plt.title('Programming language usage')

		plt.draw();
		plt.show();
		plt.savefig(fig_name);
		plt.pause(0.01);

		# file.close();
		
s.close()
