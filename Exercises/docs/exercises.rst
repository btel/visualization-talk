Visualization Exercises
=======================

Basic matplotlib: interactive mode
-----------------------------------

Advanced matplotlib: Publication-ready plots
--------------------------------------------

The goal of this exercise is to get accustomed to object-oriented interface to matplotlib and go through entire process of figure preparation - from design to the final figure ready for submission.

1. Open the supplied example of  ``mpl_template.py``.
   
   * Read comments and identify basic matplotlib artists (like lines, axes, etc.)
   * Try to determine how subclassing is used to define axes lines
     (``spines``
     in matplotlib) that provide framing and at the same time show data
     range (range frames, see Tufte, The Visual Display of Quantitative
     Information) and hide the default top ticks.

2.
 



Visualising Pubmed search on the Web
------------------------------------

The goal of this exercise is to create a simple website that will present geographic data on popularity of different research topics over the world. To this end, you will download the list of publications fulfilling your search criteria from the Pubmed, group them according to countries (based on affiliations), count them, and present the results on a world map.

*Required modules*: ``Biopython``, ``CherryPy``, ``gviz_api``

*Required files* (supplied): ``pubmed.py``, ``map_world.py``, ``page_template.html``, ``iso_contries.csv``

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
