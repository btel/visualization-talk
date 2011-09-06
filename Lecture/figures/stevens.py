# coding: utf-8
import numpy as np
from pylab import *

x = np.linspace(0,5,100)
plot(x,x, 'k-')
plot(x,x**1.5, 'r-')
plot(x,x**0.5, 'b-')
plot(x,x**0.7, 'g-')
ylim(0,5)
xlabel('stimulus magnitude')
ylabel('perceived intensity')
xticks([])
yticks([])
ax = gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
draw()
savefig('stevens.svg',transparent=True)
