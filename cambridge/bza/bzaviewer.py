#!/usr/bin/python

# Copyright 2019 Christopher Schmidt
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs

from jinja2 import Template


import sqlite3
import urllib

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def dbc():
    conn = sqlite3.connect("bza.db")
    c = conn.cursor()
    c.row_factory = dict_factory
    return c

def view(id):
    c = dbc()
    m = 0
    current = 0
    l = []
    print id
    for row in c.execute('SELECT * FROM bza where "Application Number"=?', [id]):
        return row

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        path = self.path
        if path == "/favicon.ico":
            return ""
            
        elif path == "/":
            self.index()
        else:
            id = path[1:]
            self.view(id)
    def view(self, id):
        d = open("req.html")
        template = Template( d.read() )
        item = view(id)
        data = item_data(item)
        s = template.render(**data)
        self.wfile.write(s.encode("utf-8"))
    def index(self):
        c = dbc()
        d = open("list_template.html")
        template = Template( d.read() )
        data = {'reqs':[]}
        for row in c.execute('SELECT * FROM bza order by "Application Number"'):
            data['reqs'].append(row)
        s = template.render(**data)
        self.wfile.write(s)

field_types = {
    'floor area': 'Total Gross Flr Area',
    'FAR': 'Gross Floor Area Ratio',
    'lot size/du': 'Lot Area Dwelling Unit',
    'lot width': 'Size of Lot Width',
    'lot depth': 'Size of Lot Depth',
    'front setback': 'Setbacks Front',
    'left setback': 'Setbacks Left Side',
    'right setback': 'Setbacks Right Side',
    'rear setback': 'Setbacks Rear',
    'height': 'Size of Building Height',
    'length': 'Size of Building Length',
    'width': 'Size of Building Width',
    'lot size': 'Lot Area',
    'open space': 'Usable Open Space Ratio',
    'units': 'No of Dwelling Units',
    'distance to nearest building': 'Distance to Nearest Building',
    'parking spaces': 'No of Parking Spaces',
    }
replace = {
    'Existing Size of Building Length': 'Existing Size Of Building Length',
    'Existing Lot Area': 'Exisiting Lot Area',
    'Existing Setbacks Rear': 'Existing Setbacks Back',
    'Requested Setbacks Rear': 'Requested Setbacks Back',
    'Existing Total Gross Flr Area': 'Total Gross Floor Area',
    'Requested Distance to Nearest Building': 'Requested Distance to Nearest Bldg',
    'Existing Distance to Nearest Building': 'Existing Distance to Nearest Bldg',
    'Ordinance Usable Open Space Ratio': 'Ordinance Useable Open Space Ratio',
}
def item_data(item):
    data = {'all': str(item), 'item': item}
    requests = []
    for label in field_types:
        row = {'label': label, 'change': False}
        k = field_types[label]
        for type in ['existing', 'requested', 'ordinance']:
            lookup_key = " ".join([type.title(), k])
            if lookup_key in replace:
                lookup_key = replace[lookup_key]
            row[type] = item.get(lookup_key, lookup_key)
        if row['existing'] != row['requested']:
            row['change'] = True
        requests.append(row)
        
    data['requests'] = requests
    zoning = []
    for i in range(1,7):
        k = "Zoning Ordinance Cited Section (field%s)" % i
        if item.get(k):
            zoning.append(item.get(k))
    data['zoning'] = zoning
    return data

def runweb(PORT_NUMBER):
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        
        #Wait forever for incoming htto requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
def run():
    view("BZA-004458-2014")

if __name__ == "__main__":
    runweb(8081)
