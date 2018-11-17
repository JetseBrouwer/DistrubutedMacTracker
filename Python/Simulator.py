import csv
import time


class Simulator:
	readers = []
	nodes = []
	nexts = []
	index = 0


	def __init__(self, startTime, endTime, thresholdRSSI):
		self.startTime = startTime
		self.endTime = endTime
		self.thresholdRSSI = thresholdRSSI
		pass

	def loadNode(self,  csvlocation, node):
		f = open(csvlocation, newline='')
		self.readers.append(csv.reader(f, delimiter='\t'))
		self.nodes.append(node)

		row = next(self.readers[-1])
		while round(float(row[0])) < self.startTime:
			row = next(self.readers[-1])

		# gets the first line
		self.nexts.append(row)

	def getNext(self):
		# Find newest node in next list
		nextNode = 0
		nextTime = float(2042299408.234135910)
		for i, row in enumerate(self.nexts):
			if float(row[0]) < nextTime:
				nextTime = float(row[0])
				nextNode = i

		# Get mac and time from newest in next list
		macReturn = self.nexts[nextNode][1]
		timeReturn = round(float(self.nexts[nextNode][0]))
		nodeReturn = self.nodes[nextNode]
		RSSIReturn = int(self.nexts[nextNode][4])

		# Shift newest next
		try:
			self.nexts[nextNode] = next(self.readers[nextNode])
		except StopIteration:
			del self.readers[nextNode]
			del self.nodes[nextNode]
			del self.nexts[nextNode]

		# end loop
		if nextNode > self.endTime:
			raise IndexError()

		# Remove empty mac
		if macReturn == '' or RSSIReturn < self.thresholdRSSI:
			timeReturn, macReturn, nodeReturn = self.getNext()
		else:
			# print(nextNode, time.strftime('%m/%d/%Y %H:%M:%S', timeReturn), macReturn)
			if self.index % 1000 == 0:
				print(self.index)
			self.index += 1
			nodeReturn.onPacket(timeReturn, macReturn)
		return timeReturn, macReturn, nodeReturn
