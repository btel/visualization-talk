#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of static use of Google Visualization Python API."""

__author__ = "Bartosz Telenczuk"

import gviz_api
import webserver

page_template = """
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
    
      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});
      
      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);
      
      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

      %(jscode)s
      // Set chart options
      var options = {'title':'How Much Pizza I Ate Last Night',
                     'width':400,
                     'height':300};

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
      chart.draw(jscode_data, options);
    }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
  </body>
</html>
"""



def main():

    description = [("Topping", "string"),
                    ("Slices", "number")
                    ]
    data = [
            ['Mushrooms', 3],
            ['Onions', 1],
            ['Olives', 1], 
            ['Zucchini', 1],
            ['Pepperoni', 2]
        ]

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data")
    # Creating a JSon string
    #json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
    #                        order_by="salary")

    # Putting the JS code and JSon string into the template
    html_page = page_template % vars()

    webserver.serve_page(html_page)




if __name__ == "__main__":
  main()

