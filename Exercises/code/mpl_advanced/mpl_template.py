"""
In this example for didactic reasons we will create a figure from
scratch by creating elements of the figure, such as axes, points and
lines and adding them to the figure.

This approach allows for flexible control over the presentation of
your data, avoiding, often confusing, default settings. However, in
practice, you will often combine the fexibility of object-oriented API
and the expressivity of pyplot interface (if you are not familiar with
the latter, please go to Basic matplotlib exercises).

From matplotlib maunal (http://matplotlib.sourceforge.net/users/artists.html):

"There are three layers to the matplotlib API. The
matplotlib.backend_bases.FigureCanvas is the area onto which the
figure is drawn, the matplotlib.backend_bases.Renderer is the object
which knows how to draw on the FigureCanvas, and the
matplotlib.artist.Artist is the object that knows how to use a
renderer to paint onto the canvas. The FigureCanvas and Renderer
handle all the details of talking to user interface toolkits like
wxPython or drawing languages like PostScript, and the Artist handles
all the high level constructs like representing and laying out the
figure, text, and lines. The typical user will spend 95% of his time
working with the Artists. "

In this exercises we will focus on artists.
"""


from matplotlib import rcParams

#set plot attributes
params = {'backend': 'Agg',
          'axes.labelsize': 6,
          'xtick.labelsize': 6,
          'ytick.labelsize': 6,
          'font.family': 'sans-serif',
          'axes.linewidth' : 0.5,
          'xtick.major.size' : 2,
          'ytick.major.size' : 2,
          }
rcParams.update(params)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

## this is a collection of custom artists we will use in this exercise
#  if you want to know about object-oriented mechanics used in mpl, 
#  look at the implementation and read the comments

from mpl_artists import BasicAxes

# generate some random data
t = np.arange(0.1, 9.2, 0.15)
y = t+np.random.rand(len(t)) 

#first create the figure
fig = plt.figure(figsize=(5,3))

#now define position of axes in figure coords
axes_pos = (0.18, 0.20, 0.55, 0.65) 

# create container for data markers (BasicAxes) and add it to the figure
ax1 = BasicAxes(fig, axes_pos)
fig.add_axes(ax1)

# create artists (points) based on the dataset and add them to BasicAxes container
points = mpl.lines.Line2D(t, y, marker='.',color='k',ls='', ms=4., clip_on=False)
ax1.add_line(points)

#set axis limits
ax1.set_xlim((-2, 12))
ax1.set_ylim((-2, 12))

# scale the view to show all datapoints
ax1.autoscale_view()

# uncomment to hide right-side ticks
#ax1.yaxis.set_ticks_position('left')

#set labels
ax1.set_xlabel(r'voltage (V, $\mu$V)')
ax1.set_ylabel('luminescence (L)')

#export to svg
plt.savefig('mpl_template.pdf', dpi=600)
