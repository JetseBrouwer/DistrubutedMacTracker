import time

class Node:

	# When seeing a node within 'debounce_time' seconds
	debounce_time = 30
	total_rssi_list = []

	# The maximum number of seconds a neighbor's sighting will remain in the buffer
	neighbour_buffer_time = 30 * 60

	def __init__(self, ID: str):
		# list of mac sightings by neighbors
		self.Neighbors = {}
		self.debounce_buffer = {}
		# list of all the neighbours to simulating broadcasting to them
		self.list_of_neighbors = {}
		self.ID = ID
		self.Indirect = []
		self.Direct = {}



	def setNeighbors(self, list_of_neighbors):
		# list of all the neighbours to simulating broadcasting to them
		self.list_of_neighbors = list_of_neighbors[:]
		for nodes in list_of_neighbors:
			self.Direct[nodes.ID] = []

	def broadcastPacket(self, timestamp: int, mac_address: str):
		for neighbor in self.list_of_neighbors:
			neighbor.onBroadcast(self.ID, timestamp, mac_address,)

	def onPacket(self, timestamp: int, mac_adress: str, rssi: int):
		# if self.ID == "belg":
		# 	return
		ignore = False
		# if it has been seen before            and  the difference between then and now is smaller then the debounce, ignore
		if (mac_adress in self.debounce_buffer) and (timestamp - self.debounce_buffer[mac_adress] < self.debounce_time):
			ignore = True
		self.debounce_buffer[mac_adress] = timestamp

		# check for stale entries in the buffer
		old_keys = []
		for entry in self.debounce_buffer:
			# if the node is aalready older, delete entry
			if timestamp - self.debounce_buffer[entry] > self.debounce_time:
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
						if timestamp-entries[1] > 1:
							# self.Direct.append((entries[0], entries[1], timestamp, neighbor, (timestamp-entries[1])))
							self.Direct[neighbor].append((entries[0], entries[1], timestamp, neighbor, (timestamp - entries[1])))
							self.total_rssi_list.append(rssi)
						self.Neighbors[neighbor].pop(index)
						# print("direct found")


			# Inform the other nodes about your sighting
			self.broadcastPacket(timestamp, mac_adress)

	def removeOldSightings(self, timestamp: int):
		# Check for any entry older then
		for neighbor in self.Neighbors:
			# As long as there are entries longer in the buffer then the max length, delete
			while (len(self.Neighbors[neighbor]) and timestamp - self.Neighbors[neighbor][0][1] > self.neighbour_buffer_time):
				self.Neighbors[neighbor].pop(0)
				# print("deleting old entry: ", )

	def onBroadcast(self, sender_id, timestamp: int, mac_adress: str):
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
					# print("indirect found")

		self.Neighbors[sender_id].append((mac_adress, timestamp))


if __name__ == '__main__':
	peter = Node("peter")
	klaas = Node("klaas")
	peter.setNeighbors([klaas])
	klaas.setNeighbors([peter])
	klaas.broadcastPacket(2, "123")


	peter.onPacket(4, "123")
	peter.onPacket(5, "123")

	print("je moeder, heil hitler")

