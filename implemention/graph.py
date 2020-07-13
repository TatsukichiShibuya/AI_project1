import numpy as np
import matplotlib.pyplot as plt


x = np.arange(0, 30200, 1)
y1 = 50-49.98*x/30000
y2 = 50*(0.99973923)**x

fig = plt.figure()
plt.plot(x, y1, label="y=50-49.98x/30000")
plt.plot(x, y2, label="y=50*(0.99973923)^x")
plt.legend()
plt.xlabel('time', fontsize=16)
plt.ylabel('temperature', fontsize=16)
plt.show()
fig.savefig("graph.png")
