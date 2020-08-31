import numpy as np
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

y, x = np.mgrid[:12, :11]

xcorners = x[0,0], x[0, -1], x[-1, 0], x[-1, -1]
ycorners = y[0,0], y[0, -1], y[-1, 0], y[-1, -1]
zcorners = [1, 2, 3, 4]

xy = np.column_stack([xcorners, ycorners])
xyi = np.column_stack([x.ravel(), y.ravel()])
zi = scipy.interpolate.griddata(xy, zcorners, xyi)
zi = zi.reshape(x.shape)

fig, ax = plt.subplots()
grid = ax.pcolormesh(x, y, zi)
ax.scatter(xcorners, ycorners, c=zcorners, s=200)
fig.colorbar(grid)
ax.margins(0.05)

plt.show()