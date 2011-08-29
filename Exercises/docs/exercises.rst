Visualization Exercises
=======================

Basic matplotlib: interactive mode
-----------------------------------

This tutorial covers the  basic ``pyplot`` interface of ``matplotlib``. You will use the 
interface to produce quickly efficient visualizations of your data.

1. Basic plotting

   * Generate two data arrays of equal lengths (X and Y variable).
     This could look like this::
         
         import numpy as np
         t = np.arange(0.1, 9.2, 0.15)
         #add some noise to dependent variable
         y = t+np.random.rand(len(t)) 

   * Import ``matplotlib.pyplot`` and plot the data as an XY graph::

         import matplotlib.pyplot as plt
         plt.plot(t,y)
         plt.show()

     The plot apears only after you call ``plt.show()`` (unless you
     are in interactive mode activated by ``plt.ion()``). I will omit
     the line in the following examples.

   * Label the axes by calling ``plt.xlabel`` and ``plt.ylabel``
     functions.

   * You can select line and point style passing a third format argument to
     ``plt.plot`` function. For example, to plot only points::

        plt.plot(t,y,'.')

   * Find out from the ``plt.plot`` docstring about other formats.
     Plot the data with red stars and dashed line.

2. Importing data.

   * Import the supplied CSV file ``crabs.csv``. The easiest way to do
     it is to use ``numpy.recfromcsv`` function::

         data = np.recfromcsv(``crabs.csv``)

     which returns a NumPy record array with the fields as descibed in
     Pt. 2 of Advanded matplotlib exercise.


   * Plot 4th (FL) and 5th (RW) columns against each other.

3. Escaping the flatland.

   In this exercise you will try to represent 3 different variables on
   the 2D screen using different visualization techniques.

   * Plot columns ``CL`` and ``RW`` each against ``FL`` on different
     sub-panels::

         plt.subplot(211)
         #plotting command 1
         plt.subplot(211)
         #plotting command 2

   * Plot the same panels, but arranged vertically. 

   * Plot both variables on the same panel, but using two different
     Y axes. You may add another Y axis using ``plt.twinx`` function.
     Don't forget to add labels.

   * Plot one of the variables (``CL``) as position along the Y axis
     and the other (``RW``) as a size of the circle. To this end, you
     may use the ``plt.scatter`` command.
   
   * Which of these different representations are better in showing
     the relations between these variables?  Choose
     the one you find the most efficient.


4. Grouping.

   The crab data contains measurement on crabs of different species
   and  sex (categorical variables). Group the data points belonging
   to the same species or sex using different techniques:

   * connect them by lines,

   * draw them in different colors,

   * draw them in different panels.

   * Which of the methods allows to visualize better relation between
     numerical data (size of the crab) and categorogical data? Choose
     the one you find the most efficient.

5. Final figure.
   
   * export your plot to PDF (use ``plt.savefig``)

   * Compare your final figure against the Visualization checklist.
     What might be improved? How can it be achieved in ``matplotlib``?

   * If you have time left, try to implement your ideas (or ask if you
     do not know how to start).

Congratulations, you have just learnt the basics of matplotlib and you
are ready to create your own data visualizations. I hope you enjoyed
the exercise.

**Additional resources**:

http://matplotlib.sourceforge.net/users/pyplot_tutorial.html

http://matplotlib.sourceforge.net/gallery.html


Advanced matplotlib: Publication-ready plots
--------------------------------------------

The goal of this exercise is to get accustomed to object-oriented
interface to matplotlib and go through entire process of figure
preparation - from design to the final figure ready for submission.

1. Open the supplied example of  ``mpl_template.py``.
   
   * Read comments and identify basic matplotlib artists (like lines, axes, etc.)
   * Open ``mpl_artists`` module and  try to understand how subclassing is used to define axes lines
     (``spines``
     in matplotlib) that provide framing and at the same time show data
     range (range frames, see Tufte, The Visual Display of Quantitative
     Information) and hide the default top ticks.

2. Import CSV file ``crabs.csv`` into Python. These data have 0 rows
   and 8 columns, describing 5 morphological measurements on 50 crabs
   each of two colour forms and both sexes, of the species
   Leptograpsus variegatus collected at Fremantle, W. Australia (From
   Venables & Ripley,Modern Applied Statistics with S, Springer,
   2002).

   The file contain following columns:

   * ``sp`` species - B (blue) or O (orange)
   * ``sex`` you may guess
   * ``index`` 1:50 for each group (blue male, blue female, etc.)
   * ``FL`` frontal lobe size (mm)
   * ``RW`` rear width (mm). 
   * ``CL`` carapace length (mm).
   * ``CW`` carapace width (mm).
   * ``BD`` body depth (mm).

   Recommend way of doing it is with ``numpy.recfromcsv`` function
   (returns a numpy record array introduced during the numpy lecture),
   but other alternatives are allowed (such as ``csv`` module or
   standard IO).

3. Modify the plot template to plot two of the above measurements
   against each other. Do not forget to update labels!

4. Add a third dimension to the plot using different methods (choose
   two):

   * plot two different dependent (y) variable against the same
     independent (x) variable using different markers. Use double
     y-axes to show the data dimensions (you may define a new Axes
     object of type ``mpl_artists.TwinAxes``).

   * represent the third variable with the circles of different sizes
     (Hint: use ``markersize`` keyword argument of ``Line2D``)

   * represent the third variable on a color scale, add a color bar
     to the plot

   * represent the data as a short line segments, where the position
     of line on XY plane encodes two of the variables and the angle of
     the segment encodes the third one.

   Which of the data representation is the most accurate?

5. Group variables belonging to the same crab group (blue male, blue
   female, etc., choose one method):

   * by connecting the points with a line

   * by use of color (make sure not to use colors both for representing groups
     and representing one of dependent variables)

6. Repeat exercise 4 and 5, but represent different dependent
   variables/groups in different (non-overlapping) axes.

   Does use of multiple panels increase readability?

7. Preparing publication-quality figure file. Let us assume that you
   want to prepare the final figure for submission by combining
   panels each of which contains one of the figures presented above.
   Although it is possible (and straigthforward) to do that by
   creating independent axes in the figure, often such approach poses
   several problems (for example, if the panel itself contains several
   axes, we would have to shift all of them to new positions).
   Therefore, here we will do that as a post processing step:

   * choose two of above figures and export them to SVG file.

   * modify the ``combine_svg.py`` example to read in the figures and
     move them to their final positions.

   * use inkscape from command line to export the generated SVG file
     to a format of choice, such as PDF::
     
         inkscape final_figure1.svg --export-pdf=final_figure1.pdf

   * (Optional) You may easily automate the entire process using a
     simple ``Makefile`` similar to this one (available in exercises
     directory)::

         mpl_figure1.svg : mpl_figure1.py
             python mpl_figure1.py mpl_figure1.svg

         mpl_figure2.svg : mpl_figure2.py
             python mpl_figure2.py mpl_figure2.svg

         final_figure1.svg : final_figure1.py mpl_figure1.svg mpl_figure2.svg
             python combine_svg.py
         
         %.pdf : %.svg
             inkscape $< --export-pdf=$@
      
8. "Test drive" your figure. Use the "Visualization Checklist"
   (presented during the lecture and available together with handouts)
   to test whether your figure is optimally designed. What could be
   improved?

Visualising Pubmed search on the Web
------------------------------------

The goal of this exercise is to create a simple website that will
present geographic data on popularity of different research topics
over the world. To this end, you will download the list of
publications fulfilling your search criteria from the Pubmed, group
them according to countries (based on affiliations), count them, and
present the results on a world map.

*Required modules*: ``Biopython``, ``CherryPy``, ``gviz_api``

*Required files* (supplied): ``pubmed.py``, ``map_world.py``,
``page_template.html``, ``iso_contries.csv``

At the end of this exercises, you should be able to:

* run pubmed searches ;)
* use Google Charts API to create simple visualizations,
* create a simple web application in Python,
* write simple HTML/JavaScript pages to visualize data, 

1. Use the supllied ``pubmed.py`` module to download data from pubmed and store the results in a CSV file. You will need to use the following functions:

   * ``pubmed_search``  -- returns a list of Pubmed publications on a specified topic
   * ``get_affiliation`` -- parses affiliation from the publications entries
   * ``search_countries`` -- give the list of affiliations produces a dictionary whose keys are country names and values the number of times the  country appears in the affiliation
   * ``country2csv`` -- stores the above dictionary in two-column comma-separated-files

   Don't forget to change the email address to your email (see at the top of `pubmed.py`)

#. Present the results of the Pubmed search on a map rendered in the browser.

   a) Run the sample web application ``map_world.py`` (written using CherryPy_ web framework) and open http://127.0.0.1:8080 in your browser. The script presents sample data on a map. Try hoovering over the countries with the mouse pointer. 

   b) Modify the ``map_world.py`` script to read the data from CSV file, store it in DataTable_ and pass it to the HTML page template (``page_template.html``, please take a look at the template, but do not modify it yet). You will need to modify the ``index`` method of ``HelloWorld``.

#. Add dynamic content to the map.

   So far the map shows the results of the search stored in CSV file on whichever topic you chose. However, it would be nice to allow the web-app user to specify his own search term and visualize the results. To this end, you will combine the ``pubmed.py`` module with the web framework ``map_world.py``.

   a) Add a simple form to the ``page_template.html``. It may look like this (if you know HTML the code should look familiar)::

       <form action="search" name="SearchForm" method="get">
        <input type="text" name="keyword" id="search_field" size="55">
        <input type="submit" id="updateButton" value="Search">
       </form>

   b) Run the web application. See what happens when you type in the term and click search (look at the requested URL). In order to handle the request you will only need to add a ``search``  method (or whatever you specified as an ``action`` in the above form) to ``HelloWorld``, which takes a keyword parameter called ``keyword``. For the time being, let the return value of the method be the value of the parameter. Perform the search again an see what happens... Simple, isn't it? That's CherryPy!

   c) Implement the ``search`` method to run the Pubmed search with  the term given in ``keyword`` (compare with Point 1 above), store the results in DataTable, generate a JavaScript code for this table and pass it to the page  template. Test your implementation. Pubmed searches are quite slow, so you may need to wait a while (in the meantime think how to cache the results of search, so that next time you run the same search it is faster). 

4. Homework. Combine the Pubmed searches with Google Maps... just kidding!

I hope you enjoyed this exercise!


*Additional Resources*:
 
.. _DataTable: http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html

.. _CherryPy: http://www.cherrypy.org/wiki/CherryPyTutorial

http://wiki.python.org/moin/WebProgramming 
