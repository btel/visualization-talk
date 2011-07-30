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
from webserver import DataTableHandler
from BaseHTTPServer import HTTPServer

page_template = """
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
    
      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['geochart']});
      
      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(initialize);
      
      function initialize()
      {
      var query = new google.visualization.Query('http://127.0.0.1:9000/search');
      query.send(drawChart);
      }
      

       
      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart(response) {
      
      if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
      return;
      }
      

      var data = response.getDataTable();
      // Set chart options
      var options = {};

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.GeoChart(document.getElementById('map_canvas'));
      chart.draw(data, options);
    }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="map_canvas"></div>
  </body>
</html>
"""



def serve(html_src, data_table):
    DataTableHandler.page = html_src
    DataTableHandler.data_table = data_table
    httpd = HTTPServer(("", 9000), DataTableHandler)
    print "Visit address http://127.0.0.1:9000 in your browser."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

def main():
    description = [("Country", "string"),
                    ("Count", "number")
                    ]
    
    data = []
    with open('country.csv') as f:
        for line in f.readlines():
            country, count = line.split(',')
            data.append([country, int(count)])

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data")
    # Creating a JSon string
    #json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
    #                        order_by="salary")

    # Putting the JS code and JSon string into the template
   
    serve(page_template, data_table)




if __name__ == "__main__":
  main()

