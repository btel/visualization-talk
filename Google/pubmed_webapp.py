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

import sys
sys.path.append('../Pubmed')
import gviz_api
from webserver import MyHandler
from BaseHTTPServer import HTTPServer
import urlparse
import pubmed

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
      keyword = document.getElementById('search_field').value 
      var query = new google.visualization.Query('http://127.0.0.1:9000/search?keyword=' + keyword);
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
    <form name="SearchForm">
    <input type="text" id="search_field" size="55" value="python">
    <input type="button" name="update" id="updateButton" value="Search" onClick="initialize();">
    </form>
  </body>
</html>
"""

def get_datatable(term):
    search_results = pubmed.pubmed_search(term, max_count=100) 
    aff = pubmed.get_affiliations(search_results)
    countries = pubmed.search_countries(aff)

    description = [("Country", "string"),
                    ("Count", "number")
                    ]
    
    data = list(countries.items())
    
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    return data_table

class PubmedHandler(MyHandler):
    
    
    def do_GET(self):
        """Respond to a GET request."""
        url_parsed = urlparse.urlparse(self.path)
        path = url_parsed.path.lstrip("/")
        print url_parsed, path
        #import pdb; pdb.set_trace()
        if path == '':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.page)
        elif path == 'search':
            query = urlparse.parse_qs(url_parsed.query)
            keyword = query.setdefault("keyword", "python")
            tqx = dict([q.split(':') for q in query['tqx'][0].split(';')])
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            data_table = get_datatable(keyword)
            content = data_table.ToJSonResponse(req_id=int(tqx['reqId']))
            self.wfile.write(content)


def serve(html_src):
    PubmedHandler.page = html_src
    httpd = HTTPServer(("", 9000), PubmedHandler)
    print "Visit address http://127.0.0.1:9000 in your browser."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

def main():
    serve(page_template)




if __name__ == "__main__":
  main()

