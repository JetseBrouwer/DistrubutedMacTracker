import csv
import time

class Simulator:

	def __init__(self, startTime, endTime, thresholdRSSI, mac_list = []):
		self.startTime = startTime
		self.endTime = endTime
		self.thresholdRSSI = thresholdRSSI
		self.readers = []
		self.nodes = []
		self.nexts = []
		self.index = 0
		self.mac_list = mac_list

		pass

	def loadNode(self,  csvlocation, node):
		f = open(csvlocation, newline='')
		self.readers.append(csv.reader(f, delimiter='\t'))
		self.nodes.append(node)

		row = next(self.readers[-1])
		while round(float(row[0])) < self.startTime:
			row = next(self.readers[-1])

		print("Node", node.ID, "Starts on", time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(float(row[0]))), float(row[0]))

		# gets the first line
		self.nexts.append(row)

	def getNext(self):
		do = True
		while do:
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
			if timeReturn > self.endTime:
				print("Node", nodeReturn.ID, "Stops on", time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(timeReturn)), timeReturn)
				raise IndexError()

			# Remove empty mac
			if not (macReturn == '' or RSSIReturn < self.thresholdRSSI or ((not self.mac_list == []) and (macReturn not in self.mac_list))):
				do = False


		# print(nextNode, time.strftime('%m/%d/%Y %H:%M:%S', timeReturn), macReturn)
		if self.index % 1000 == 0:
			print(self.index)
		self.index += 1
		nodeReturn.onPacket(timeReturn, macReturn, RSSIReturn)
		return timeReturn, macReturn, nodeReturn
