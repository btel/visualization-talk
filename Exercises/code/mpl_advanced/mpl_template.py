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
          'axes.titlesize': 8,
          'legend.fontsize': 6,
          'xtick.labelsize': 6,
          'ytick.labelsize': 6,
          'font.family': 'sans-serif',
          'axes.linewidth' : 0.5,
          'xtick.major.size' : 2,
          'ytick.major.size' : 2,
          'font.size' : 8,
          'xaxis.major.size': 2,
          }
rcParams.update(params)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.axes, matplotlib.spines, matplotlib.axis
import matplotlib.lines, matplotlib.path

class DataRangeSpine(mpl.spines.Spine):

    def cla(self):
        """Clear the current spine"""
        self._position = ("axes",0) 
        if self.axis is not None:
            self.axis.cla()
   
    #make the spines scale with data
    def _adjust_location(self):
        v1 = self._path.vertices[:]
        if self.spine_type=='left':
            low,high = self.axes.dataLim.intervaly
            v1[0,1] = low
            v1[1,1] = high
        elif self.spine_type=='bottom':
            low,high = self.axes.dataLim.intervalx
            v1[0,0] = low
            v1[1,0] = high
        else:
            raise ValueError('unknown spine spine_type: %s'%self.spine_type)

        self._path.vertices = v1 
    
## Subclass matplotlib.axis.XAxis to hide top ticks. 
# You could do
# the same at runtime using set_ticks_position (see below)

class XAxis(mpl.axis.XAxis):
    def _get_tick(self, major):
        return mpl.axis.XTick(self.axes, 0, '', tick2On=False, label2On=False, major=major)

class BasicAxes(mpl.axes.Axes):
    """Custom Axes class that contains only two spines like
    "old-school" plots."""
    
    def _init_axis(self):
        # here we use our subclassed Axis class 
        self.xaxis = XAxis(self)
        self.yaxis = mpl.axis.YAxis(self)
        self.spines['horizontal'].register_axis(self.xaxis)
        self.spines['vertical'].register_axis(self.yaxis)
        self._update_transScale()

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        return {
                'vertical':DataRangeSpine.linear_spine(self,'left'),
                'horizontal':DataRangeSpine.linear_spine(self,'bottom'),
               }
    
    def get_xaxis_transform(self,which='grid'):
        return self._xaxis_transform
    
    def get_yaxis_transform(self,which='grid'):
        return self._yaxis_transform


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
ax1.set_xlim((-5, 15))

#repositions spines
ax1.spines['vertical'].set_position(('axes',0))

# scale the view to show all datapoints
ax1.autoscale_view()

# uncomment to hide right-side ticks
#ax1.yaxis.set_ticks_position('left')

#set labels
ax1.set_xlabel(r'voltage (V, $\mu$V)')
ax1.set_ylabel('luminescence (L)')

#export to svg
plt.savefig('mpl_template.pdf', dpi=600)
