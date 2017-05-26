import numpy as np
import matplotlib.pyplot as plt
import os
import random 

while True:
	file = False
	while file == False:
		filePath = raw_input("\nPlease type path to the file with Data...")
		if os.path.isfile(filePath):
			file = True
		else:
			print '\nFile not found'

	file = open(filePath,'r') 
	listCreated = False
	elements = []
	xLabel = []
	X = []
	for line in file:
		if listCreated == False: 
			print line
			line = line.replace('\n', '')
			line = line.split('|')
			dis = {}
			for element in line:
				elements.append(element)
				dis[element] = []
			print dis
			listCreated = True
		else:	
			line = line.replace('\n', '')
			line = line.split('|')
			xLabel.append(line.pop(0))
			del line[-1]
			print line
			index = 0
			for element in line:
				dis[elements[line.index(element)]].append(element)
	print dis
	
	for x in xLabel:
		X.append(xLabel.index(x)+1)
		
	cmap = plt.get_cmap('jet')
	colors = cmap(np.linspace(0, 1, len(dis)))
	print(colors)
	
	
	for element,color in zip(elements,colors):
		x = np.array(X)
		y = np.array(dis[element])
		#plt.xticks(x, xLabel)
		plt.plot(x, y, label=element, c=color)
	plt.legend()
	plt.show()
