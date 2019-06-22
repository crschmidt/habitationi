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

def get_caps(options):
    far = {}
    for i in ['A-1', 'A-2', 'B', 'SD-2']:
        far[i] = 0.5
    for i in ['C', 'SD-9', 'SD-10F', 'SD-10H']:
        far[i] = 0.6
    for i in ['C-1', 'BA-3', 'IB-2', 'O-1']:
        far[i] = .75
    for i in ['BA-1', 'SD-12']:
        far[i] = 1.0
    for i in ['C-1A', 'SD-5']:
        far[i] = 1.25
    for i in ['IA-1', 'IA', 'O-2A', 'SD-4A', 'SD-13']:
        far[i] = 1.5
    for i in ['C-2', 'C-2B', 'BA', 'BA-2', 'SD-8']:
        far[i] = 1.75
    for i in ['BC', 'O-2']:
        far[i] = 2.0
    for i in ['C-2A']:
        far[i] = 2.50
    for i in ['C-3', 'C-3A', 'C-3B', 'BB', 'BB-2', 'BC-1', 'IB-1', 'O-3', 'O-3A', 'SD-1', 'SD-6', 'SD-7']:
        far[i] = 3.0
    for i in ['IA-2', 'IB']:
        far[i] = 4.0
    far['BB-1'] = 3.25
    far['SD-11'] = 1.7
    far['SD-15'] = 3.5
    lot_area = {
            'A-1': 6000,
            'A-2': 4500,
            'C-1A': 1000,
            'BC': 500,
            'BC-1': 450,
            'IA-1': 700,
            'SD-8': 650,
            'SD-14': 800,
        }
    for i in ['IB-2', 'BA-1']:
        lot_area[i] = 1200
    for i in ['B', 'SD-2', 'SD-3']:
        lot_area[i] = 2500
    for i in ['C', 'SD-10F', 'SD-10H', 'SD-9']:
        lot_area[i] = 1800
    for i in ['C-1', 'BA-3']:
        lot_area[i] = 1500
    for i in ['C-2', 'C-2B', 'O-2', 'BA', 'BA-2', 'SD-4', 'SD-4A', 'SD-5', 'SD-11', 'SD-13']:
        lot_area[i] = 600
    for i in ['C-2A', 'C-3', 'C-3A', 'C-3B', 'BB', 'BB-1', 'BB-2', 'SD-1', 'SD-6', 'SD-7']:
        lot_area[i] = 300
    
    for i in lot_area:
        if options and 'lot_explicit' in options:
            lot_area[i] = options['lot_explicit']
        elif options and 'lot_factor' in options:
            lot_area[i] = int(lot_area[i] / float(options['lot_factor']))
    if 'no_lot' in options:
        lot_area = {}
    for i in far:
        if options and 'far_explicit' in options:
            far[i] = options['far_explicit']
        elif options and 'far_factor' in options:
            far[i] = far[i] * float(options['far_factor'])
    if 'no_far' in options:
        far = {}
    return far, lot_area


def table(options):
    far, lot_area = get_caps(options)
    table = []
    for i in ['A-1', 'A-2', 'B', 'C', 'C-1', 'C-1A', 'C-2', 'C-2A', 'C-2B', 'C-3', 'C-3A', 'C-3B']:
        table.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (i, far.get(i, ""), lot_area.get(i,"")))
    return "\n".join(table)    

def unit_cap(row, options=None):
    if not options:
        options = {}
    
    far, lot_area = get_caps(options)

    zone = row['zone']
    if (not zone.startswith("C") and not zone in ("A-1", "A-2", "B")) or zone == "CRDD":
        return -1
    
    if zone in ['A-1', 'A-2'] and not 'no_a' in options:
        return 1
    #print row
    area = float(row.get('gis_lot_size',0) or 0)
    if zone in lot_area and area:
        m = max(area/(lot_area[zone]), 1)
    else:
        m = 100000
    max_building = area * far[zone] * 1
    if max(int(max_building/800), 1) < m:
        m = max(int(max_building/800), 1)
    if zone == "B" and not 'no_b' in options:
        m = min(m, 2)
    return m    

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def compute_count(options = None):
    conn = sqlite3.connect("prop.db")
    if options == None:
        options = {}
    c = conn.cursor()
    c.row_factory = dict_factory
    m = 0
    current = 0
    for row in c.execute("SELECT * FROM lots"):
        t = unit_cap(row, options=options)
        if t == -1:
            continue
        m += int(t)
    return m

def describe(options):
    changes = []
    if 'no_lot' in options:
        changes.append("eliminate lot size/unit minimums")
    elif 'lot_explicit' in options:
        changes.append("set all lot size/unit minimums to %s" % options['lot_explicit'])
    elif 'lot_factor' in options and options['lot_factor'] != 1.0:    
        changes.append('decrease lot size minimums by a factor of %s' % options['lot_factor'])
    if 'no_a' in options:
        changes.append('eliminate single family zoning in A-1 and A-2 zones')
    if 'no_b' in options:
        changes.append('eliminate two-family zoning limits in B zones')
    if 'far_explicit' in options:
        changes.append("set all FAR maximums to %s" % options['far_explicit'])
    elif 'far_factor' in options and options['far_factor'] != 1.0:
        changes.append('increase FAR maximums by a factor of %s' % options['far_factor'])

    if len(changes):

        return ", ".join(changes)
    else:
        return ""

def serve(options):
    d = open("unit_template.html")
    template = Template( d.read() )
    unit_count = int(compute_count(options))
    data = {}
    data['changes'] = describe(options)
    data['unit_count'] = unit_count
    data['increase'] = unit_count-37453
    data['table'] = table(options) 
    data['options'] = options
    s = template.render(**data)
    return s

PORT_NUMBER = 8080

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        form = parse_qs(urlparse(self.path).query)
        options = {}
        for i in ['far_factor', 'lot_factor']:
            if i in form:
                options[i] = float(form[i][0])
            else:
                options[i] = 1.0
        if 'far_explicit' in form and form['far_explicit']:
            options['far_explicit'] = float(form['far_explicit'][0])
        if 'lot_explicit' in form and form['lot_explicit']:
            options['lot_explicit'] = int(form['lot_explicit'][0])
        if 'lot' in form:
            options['no_lot'] = True
        if 'singlefamily' in form:
            options['no_a'] = True
        if 'twofamily' in form:
            options['no_b'] = True
        self.wfile.write(serve(options))
        return

def run():
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

if __name__ == "__main__":
    print run()
