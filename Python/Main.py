import time
from NodeAlgorithm import Node
from Simulator import Simulator

import numpy
# import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



from calendar import timegm

print("Started")

patricia = Node("patricia")
belg = Node("belg")
memphis = Node("memphis")

mac_niels = '94:65:2d:2d:14:17'
mac_david = '88:BD:45:AB:D5:8A'
mac_jetse = '34:80:b3:91:e1:c7'

mac_list = [mac_niels, mac_david, mac_jetse]



patricia.setNeighbors([belg, memphis])
memphis.setNeighbors([belg, patricia])
belg.setNeighbors([patricia, memphis])

#
# simulator = Simulator(1542294900, 1542298500, -150)
# simulator.loadNode("Measurements/2018-11-15/output_jetse.csv", patricia)
# simulator.loadNode("Measurements/2018-11-15/output_david.csv", belg)
# simulator.loadNode("Measurements/2018-11-15/output_nielsch.csv", memphis)


# simulator.loadNode("Measurements/2018-11-15/klein.csv", 5)


simulator = Simulator(1542447000, 1542450600, -150)
simulator.loadNode("Measurements/2018-11-17/output_jetse.csv", patricia)
simulator.loadNode("Measurements/2018-11-17/output_david.csv", belg)
simulator.loadNode("Measurements/2018-11-17/output_nielsch.csv", memphis)

i = 0
while True:
    try:
        simulator.getNext()
        i += 1
    except IndexError:
        break
print(i)
print("Done")

# the histogram of the data
x = patricia.total_rssi_list
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

# # add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('RSSI')
plt.ylabel('Sightings')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([-100, -30, 0, 0.03])
plt.grid(True)

plt.show()

# EXport Niels' measurmenets
print("jetse-> niels", len(memphis.Direct["patricia"]))
print(memphis.Direct["patricia"][0])
numpy.savetxt("jetse-to-niels.csv", memphis.Direct["patricia"], delimiter=", ", fmt="%s")
print("david-> niels", len(memphis.Direct["belg"]))
numpy.savetxt("david-to-niels.csv", memphis.Direct["belg"], delimiter=", ", fmt="%s")

# Export Jetse's measurements
print("niels-> jetse", len(patricia.Direct["memphis"]))
numpy.savetxt("niels-to-jetse.csv", patricia.Direct["memphis"], delimiter=", ", fmt="%s")
print("david-> jetse", len(patricia.Direct["belg"]))
numpy.savetxt("david-to-jetse.csv", patricia.Direct["belg"], delimiter=", ", fmt="%s")

#export
print("jetse-> david", len(belg.Direct["patricia"]))
numpy.savetxt("jetse-to-david.csv", belg.Direct["patricia"], delimiter=", ", fmt="%s")
print("niels-> david", len(belg.Direct["memphis"]))
numpy.savetxt("niels-to-david.csv", belg.Direct["memphis"], delimiter=", ", fmt="%s")

print("done")
# print(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(1542447000)))
# print(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(1542450600)))
# # utc_time = time.strptime("2018/11/17 09:30:00 ", "%Y/%m/%d %H:%M:%S")
# # utc_time = time.strptime("2018/11/17 09:30:00", "%Y/%m/%d %H:%M:%S") # 1542447000
# utc_time = time.strptime("2018/11/17 10:30:00", "%Y/%m/%d %H:%M:%S") #1542450600
# epoch_time = timegm(utc_time)
#
# print(epoch_time)