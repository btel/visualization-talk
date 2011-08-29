#!/usr/bin/env python
#coding=utf-8

import svgutils.transform as sg

# open source svg files 
# (for sake of example we read the same file twice)
fig1 = sg.fromfile('mpl_template.svg')
fig2 = sg.fromfile('mpl_template.svg')

# get the root of figure code
plot1 = fig1.getroot()
plot2 = fig2.getroot()

# create a new figure of specified size
fig = sg.SVGFigure("12cm", "13cm")

# move the plots
plot1.moveto(0,0)
plot2.moveto(200, 0)

# add text labels
txt1 = sg.TextElement(25,20, "A", size=12, weight="bold")
txt2 = sg.TextElement(225,20, "B", size=12, weight="bold")

fig.append([plot1, plot2])
fig.append([txt1, txt2])

# save figures
fig.save('final_figure1.svg')
