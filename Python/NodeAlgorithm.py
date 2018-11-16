import time

class Node:
	# list of mac sightings by neighbors
	Neighbors = {}
	# list of all the neighbours to simulating broadcasting to them
	list_of_neighbors = []
	ID = ""
	Indirect = []
	Direct = []
	# When seeing a node within 'debounce_time' seconds
	debounce_time = 30
	debounce_buffer = {}
	# The maximum number of seconds a neighbor's sighting will remain in the buffer
	neighbour_buffer_time = 30 * 60

	def __init__(self, ID: str):
		self.ID = ID

	def setNeighbors(self, list_of_neighbors):
		self.list_of_neighbors = list_of_neighbors

	def broadcastPacket(self, timestamp: float, mac_address: str):
		for neighbor in self.list_of_neighbors:
			neighbor.onBroadcast(self.ID, timestamp, mac_address,)

	def onPacket(self, timestamp: float, mac_adress: str):
		# On reception of the mac check if it hasn't been seen the last 'debounce_tine' seconds
		ignore = False
		# if it has been seen before          and  the difference between then and now is smaller then the debounce, ignore
		if (mac_adress in self.debounce_buffer) and (timestamp - self.debounce_buffer[mac_adress]  < self.debounce_time):
			ignore = True
		self.debounce_buffer[mac_adress] = timestamp

		# check for stale entries in the buffer
		for entry in self.debounce_buffer:
			# if the node is aalready older, delete entry
			if timestamp - self.debounce_buffer[entry]  > self.debounce_time:
				self.debounce_buffer.pop(entry)

		if not ignore:
			self.removeOldSightings(timestamp)
			# check if this mac has been seen by other nodes before


			# if receive a MAC broadcast, i also check if it has been seen previously by another surrounding node.
			# If this is the case i remove it from that list, and place it in the senders list. (and report it as an direct walk)

			for neighbor in self.Neighbors:
				for entries in self.Neighbors[neighbor]:
					if entries[0] == mac_adress:
						self.Direct.append((entries[0],entries[1], timestamp))

			# Inform the other nodes about your sighting
			self.broadcastPacket(timestamp, mac_adress)


	def removeOldSightings(self, timestamp: float):
		# Check for any entry older then
		for neighbor in self.Neighbors:
			# As long as there are entries longer in the buffer then the max length, delete
			while (timestamp - self.Neighbors[neighbor][0][1] > self.neighbour_buffer_time):
				print("deleting old entry: " + self.Neighbors[neighbor].pop(0))


	def onBroadcast(self, sender_id, timestamp: float, mac_adress: str):
		self.removeOldSightings(timestamp)

		# if this is the first message of the node create a buffer for it
		if sender_id not in self.Neighbors:
			self.Neighbors[sender_id] = []

		# if receive a MAC broadcast, i also check if it has been seen previously by another surrounding node.
		# If this is the case i remove it from that list, and place it in the senders list. (and report it as an indirect walk)

		for neighbor in self.Neighbors:
			for entries in self.Neighbors[neighbor]:
				if entries[0] == mac_adress:
					self.Indirect.append((entries[0], entries[1], timestamp))

		self.Neighbors[sender_id].append((mac_adress, timestamp))



if __name__ == '__main__':
	peter = Node("peter")
	klaas = Node("klaas")
	peter.setNeighbors([klaas])
	klaas.setNeighbors([peter])
	klaas.broadcastPacket(2, "123")
	peter.onPacket(3, "123")