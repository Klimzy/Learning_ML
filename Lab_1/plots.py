import numpy as np
from matplotlib import pyplot as plt
import seaborn as sb


def sinplot (flip = 1):
   x = np.linspace(0, 35, 100)
   plt.plot(x, (0.8 * np.cos(3 * x) + np.cos(x)) * (x-4))

sb.set()
sinplot()
plt.show()