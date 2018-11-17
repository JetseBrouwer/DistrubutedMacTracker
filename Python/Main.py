import time
from NodeAlgorithm import Node
from Simulator import Simulator
from calendar import timegm

print("Started")

patricia = Node("patricia")
belg = Node("belg")
memphis = Node("memphis")

patricia.setNeighbors([belg, memphis])
memphis.setNeighbors([belg, patricia])
belg.setNeighbors([patricia, memphis])

# simulator = Simulator(1542294900, 1542298500, -85)
simulator = Simulator(1542447000, 1542450600, -100)
simulator.loadNode("Measurements/2018-11-17/output_jetse.csv", patricia)
simulator.loadNode("Measurements/2018-11-17/output_david.csv", belg)
simulator.loadNode("Measurements/2018-11-17/output_nielsch.csv", memphis)
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

# print(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(1542447000)))
# print(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(1542450600)))
# # utc_time = time.strptime("2018/11/17 09:30:00 ", "%Y/%m/%d %H:%M:%S")
# # utc_time = time.strptime("2018/11/17 09:30:00", "%Y/%m/%d %H:%M:%S") # 1542447000
# utc_time = time.strptime("2018/11/17 10:30:00", "%Y/%m/%d %H:%M:%S") #1542450600
# epoch_time = timegm(utc_time)
#
# print(epoch_time)