import time
from NodeAlgorithm import Node
from Simulator import Simulator


print("Started")


patricia = Node("patricia")
belg = Node("belg")
memphis = Node("memphis")

simulator = Simulator()
simulator.loadNode("Measurements/2018-11-15/output_jetse.csv", patricia)
simulator.loadNode("Measurements/2018-11-15/output_david.csv", belg)
simulator.loadNode("Measurements/2018-11-15/output_nielsch.csv", memphis)
# simulator.loadNode("Measurements/2018-11-15/klein.csv", 5)



i = 0
while True:
	try:
		simulator.getNext()
		i += 1
		# print(time.strftime('%m/%d/%Y %H:%M:%S', timeNode), Nodemac)
	except IndexError:
		break
print(i)
print("Done")



