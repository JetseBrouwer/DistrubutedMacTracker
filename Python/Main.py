import time
from NodeAlgorithm import Node
from Simulator import Simulator

print("Started")

patricia = Node("patricia")
belg = Node("belg")
memphis = Node("memphis")

patricia.setNeighbors([belg, memphis])
memphis.setNeighbors([belg, patricia])
belg.setNeighbors([patricia, memphis])

simulator = Simulator(1542294900, 1542298500, -85)
simulator.loadNode("Measurements/2018-11-15/output_jetse_crop.csv", patricia)
simulator.loadNode("Measurements/2018-11-15/output_david_crop.csv", belg)
simulator.loadNode("Measurements/2018-11-15/output_nielsch_crop.csv", memphis)
# simulator.loadNode("Measurements/2018-11-15/klein.csv", 5)


i = 0
while True:
    try:
        simulator.getNext()
        i += 1
    except IndexError:
        break
print(i)
print("Done")

# print(time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(1542294095.959328761)))
