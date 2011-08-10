#!/usr/bin/env python
#coding=utf-8

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
        elif self.spine_type in ['bottom', 'top']:
            low,high = self.axes.dataLim.intervalx
            v1[0,0] = low
            v1[1,0] = high
        else:
            raise ValueError('unknown spine spine_type: %s'%self.spine_type)

        self._path.vertices = v1 
    
## Subclass matplotlib.axis.XAxis to hide top ticks. 
# You could do
# the same at runtime using set_ticks_position (see below)

class BottomAxis(mpl.axis.XAxis):
    def _get_tick(self, major):
        #tick2On and label2On determine whether to show top ticks
        return mpl.axis.XTick(self.axes, 0, '', tick2On=False, label2On=False, major=major)

class TopAxis(mpl.axis.XAxis):
    def _get_tick(self, major):
        #tick1On and label1On determine whether to show bottom ticks
        return mpl.axis.XTick(self.axes, 0, '', tick1On=False, label1On=False, major=major)

class BasicAxes(mpl.axes.Axes):
    """Custom Axes class that contains only two spines like
    "old-school" plots."""
    
    def _init_axis(self):
        # here we use our subclassed Axis class 
        self.xaxis = BottomAxis(self)
        self.yaxis = mpl.axis.YAxis(self)
        
        #repositions spines
        self.spines['horizontal'].set_position(('axes', 0))
        self.spines['vertical'].set_position(('axes', 0))
        
        
        self.spines['horizontal'].register_axis(self.xaxis)
        self.spines['vertical'].register_axis(self.yaxis)
        self._update_transScale()

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        return {
                'vertical':DataRangeSpine.linear_spine(self,'left'),
                'horizontal':DataRangeSpine.linear_spine(self,'top'),
               }
    
    def get_xaxis_transform(self,which='grid'):
        return self._xaxis_transform
    
    def get_yaxis_transform(self,which='grid'):
        return self._yaxis_transform
