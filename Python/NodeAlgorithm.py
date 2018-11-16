import time

class Node:

	# When seeing a node within 'debounce_time' seconds
	debounce_time = 30

	# The maximum number of seconds a neighbor's sighting will remain in the buffer
	neighbour_buffer_time = 6000 * 60

	def __init__(self, ID: str):
		# list of mac sightings by neighbors
		self.Neighbors = {}
		self.debounce_buffer = {}
		# list of all the neighbours to simulating broadcasting to them
		self.list_of_neighbors = {}
		self.ID = ID
		self.Indirect = []
		self.Direct = []



	def setNeighbors(self, list_of_neighbors):
		# list of all the neighbours to simulating broadcasting to them
		self.list_of_neighbors = list_of_neighbors[:]

	def broadcastPacket(self, timestamp: float, mac_address: str):
		for neighbor in self.list_of_neighbors:
			neighbor.onBroadcast(self.ID, timestamp, mac_address,)

	def onPacket(self, timestamp: float, mac_adress: str):
		ignore = False
		# if it has been seen before            and  the difference between then and now is smaller then the debounce, ignore
		if (mac_adress in self.debounce_buffer) and (timestamp - self.debounce_buffer[mac_adress]  < self.debounce_time):
			ignore = True
		self.debounce_buffer[mac_adress] = timestamp

		# check for stale entries in the buffer
		old_keys = []
		for entry in self.debounce_buffer:
			# if the node is aalready older, delete entry
			if timestamp - self.debounce_buffer[entry]  > self.debounce_time:
				old_keys.append(entry)

		for keys in old_keys:
			self.debounce_buffer.pop(keys)
		old_keys.clear()

		if not ignore:
			self.removeOldSightings(timestamp)

			# if receive a MAC broadcast, i also check if it has been seen previously by another surrounding node.
			# If this is the case i remove it from that list, and place it in the senders list. (and report it as an direct walk)

			for neighbor in self.Neighbors:
				# for entries in self.Neighbors[neighbor]:
				for index, entries in enumerate(self.Neighbors[neighbor]):
					if entries[0] == mac_adress:
						self.Direct.append((entries[0], entries[1], timestamp))
						self.Neighbors[neighbor].pop(index)


			# Inform the other nodes about your sighting
			self.broadcastPacket(timestamp, mac_adress)


	def removeOldSightings(self, timestamp: float):
		# Check for any entry older then
		for neighbor in self.Neighbors:
			# As long as there are entries longer in the buffer then the max length, delete
			while (len(self.Neighbors[neighbor]) and timestamp - self.Neighbors[neighbor][0][1] > self.neighbour_buffer_time):
				print("deleting old entry: ", self.Neighbors[neighbor].pop(0))


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
	# klaas.broadcastPacket(2, "123")


	peter.onPacket(4, "123")
	peter.onPacket(5, "123")