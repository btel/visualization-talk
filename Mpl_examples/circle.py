#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (C) 2011  Nicolas P. Rougier
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the glumpy Development Team nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# -----------------------------------------------------------------------------
import string
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as m_path
import matplotlib.patches as m_patches


# Data to be represented
# ----------
n = 100
def gen_label(min_size, max_size):
    return "".join([random.choice(string.letters)
                    for i in xrange(random.randint(min_size,max_size))] )
labels = ["%d. %s" % (i+1,gen_label(10,15)) for i in range(n)]

links = np.zeros((n,n))
for i in range(5):    
    links[np.random.randint(n-1),:] = np.random.random(n) > 0.5
# ----------


# Choose some colors and reduce figure size such that labels fit
matplotlib.rc('axes', facecolor = 'white')
matplotlib.rc('figure.subplot', left   = .2)
matplotlib.rc('figure.subplot', right  = .8)
matplotlib.rc('figure.subplot', bottom = .2)
matplotlib.rc('figure.subplot', top    = .8)


# Make figure background the same colors as axes 
fig = plt.figure(figsize=(12,12), facecolor='white')

# Use a polar axes
axes = plt.subplot(111, polar=True)

# No ticks, we'll put our own
plt.xticks([])
plt.yticks([])

# Set y axes limit
plt.ylim(0,10)


# Ring color from y=9 to y=10
theta = np.arange(np.pi/n, 2*np.pi, 2*np.pi/n)
radii = np.ones(n)*10
width = 2*np.pi/n
bars  = axes.bar(theta, radii, width=width, bottom=9, edgecolor='w',
                 lw = 2, facecolor = '.9')
for i,bar in enumerate(bars):
    bar.set_facecolor( plt.cm.jet(i/float(n)))


# Draw lines between connected nodes
for i in range(n):
    for j in range(n):
        if not links[i,j]: continue

        # Start point
        t0,r0 = i/float(n) * 2 * np.pi, 9

        # End point
        t1,r1 = j/float(n) * 2 * np.pi, 9

        # Some noise in start end and end point
        t0 += .5*np.random.uniform(-np.pi/n,+np.pi/n)
        t1 += .5*np.random.uniform(-np.pi/n,+np.pi/n)

        verts = [ (t0,r0), (t1,5), (t1,r1) ]
        codes = [m_path.Path.MOVETO, m_path.Path.CURVE3, m_path.Path.LINETO]
        path  = m_path.Path(verts,codes)

        # This filled polygon is not really necessary but it gives a nice
        # overall colorization
        patch = m_patches.PathPatch(path, fill=True, edgecolor='blue',
                                    linewidth=0, alpha=.01)
        axes.add_patch(patch)

        # Actual line
        patch = m_patches.PathPatch(path, fill=False, edgecolor='blue',
                                    linewidth=.5, alpha=.05)
        axes.add_patch(patch)


# First, we measure the unit in screen coordinates
x0,y0 = axes.transData.transform_point((0.0, 0.0))
x1,y1 = axes.transData.transform_point((0.0, 1.0))
unit = float(x1-x0)


plt.ion()
for i in range(len(labels)):
    angle_rad = i/float(len(labels))*2*np.pi
    angle_deg = i/float(len(labels))*360
    label = plt.text(angle_rad, 10.5, labels[i], size=10, rotation=0,
                     horizontalalignment='center', verticalalignment="center")

    # To get text measure, we have to draw it first
    plt.draw()

    # Compute the text extent in data coordinate
    w = label.get_window_extent().width / unit

    # Adjust anchor point and angle
    label.set_y(10.5 + w/2.0)
    label.set_rotation(angle_deg)
plt.ioff()


# Done
plt.savefig('circle.png', facecolor='white')
plt.show()
