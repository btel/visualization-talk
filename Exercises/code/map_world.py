import cherrypy
import os, sys
import gviz_api

current_dir = os.path.dirname(os.path.abspath(__file__))

class HelloWorld:
   
    @cherrypy.expose
    def index(self):
       
        # Preparing data 
        description = [("Country", "string"),
                        ("Count", "number")
                        ]
        
        data = [('GB', 21),
                ('POLAND', 21),
                ('GERMANY', 5), 
                ('US', 1)]
        
        # Populating data table
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        # Creating a JavaScript representation of data_table
        jscode = data_table.ToJSCode("jscode_data")
        
        # Reading a page template
        with file(os.path.join(current_dir, "page_template.html"), 'r') as f:
            template = f.read()
        
        # Putting the JS code into the template using python string formatting
        html_page = template % {'jscode': jscode}
        
        return html_page   
    
cherrypy.quickstart(HelloWorld())
