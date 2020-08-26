#!/usr/bin/python

# Copyright 2020 Christopher Schmidt
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


import sqlite3
import urllib


class_lookup = {
'SINGLE FAMILY': 'Single family home',
'CONDO': 'Condo building',
'TWO FAMILY': 'Two family home',
'THREE FAMILY': 'Three family home',
'APT 4-8 UNIT': 'Small apartment building',
'APTS 9+ UNIT': 'Large apartment building',
'TOWN OWNED': 'City property',
'VACANT LAND': 'Vacant land',
'RETAIL STORE': 'Retail store',
'RES/COMM': 'Mixed Residential/Commercial',
'OUT BLDG': 'Out Building',
'MULT HOUSES': 'Multiple houses',
'RES-UNDEV': 'Undevelopable residential',
'RELIGIOUS': 'Religious building',
'PSCHOOL': 'Private school',
#OFFICE|42
#COMM/RES|35
#COMM MASS|24
#LODGING|23
#CHARITABLE|22
'PARKLOT': 'Parking lot',
#AUTHORITIES|13
#AUTO REPAIR|12
#COMM-UNDEV|12
#CONDO PARK|12
#RST/BAR|12
#MEDICAL OFFICE|11
#RES-PARK-LOT|11
#BANK|9
#US GOVT|9
#SERVICE ST|8
#AFFORD-MULTI-UNITS|7
#CHILD CARE|7
#INN|7
#OFFICE CONDO|7
#COMMERCIAL|6
'ELECSUB': "Electric Substation",
#EXEM/COMM|6
#COMM CONDO|5
#HOTEL|5
#POTENTL DEV|5
#COMM WHS|4
#HOSPITAL|4
'PARKGAR': 'Parking Garage',
#PARKGAR|4
#AFFORD-CONDOS|3
#COMM/EXM|3
#CONSERVATION|3
#OTHER|3
#SUPERMARKET|3
#AUTO SALES|2
#FRATERNITY|2
#FUNERAL HOME|2
#HEALTH CLUB|2
#OTH M/V|2
#RES/EXEMPT|2
#SCHOOL|2
#ASSTD LIVING|1
#CARWASH|1
#CONDO PRK-LOT|1
#EXEM/RES|1
#FOREIGN CONS|1
#FRATERNAL|1
#GROUP HOME|1
#IN RECR|1
#NURSING HOME|1
'RES/61A': 'Residential/agricultural',
'61A/RES': 'Residential/agricultural',
#TEL XST|1
#TENNIS|1
}
    
zone_map = {
        'F-1': 'F-1.0',
        'G(DP)': 'G-(DP)',
        'G10': 'G-1.0',
        'G175(CC)': 'G-1.75',
        'G175(LSH)': 'G-1.75(LSH)',
        'G175(WS)': 'G-1.75',
        'G-1.75(CC)': 'G-1.75',
        'G-1.75(LSH)': 'G-1.75(LSH)',
        'G-1.75(WS)': 'G-1.75',
        'G20': 'G-2.0',
        'G20(CA)': 'G-2.0',
        'G-2.0(CA)': 'G-2.0',
        'GMR20': 'GMR-2.0',
        'I(EISD)': 'I-(EISD)',
        'I10': 'I-1.0',
        'L05': 'L-0.5',
        'L05(CL)': 'L-0.5',
        'L-0.5(CL)': 'L-0.5',
        'L10': 'L-1.0',
        'M05': 'M-0.5',
        'M10': 'M-1.0',
        'M10(CAM)': 'M-1.0',
        'M-1.0(CAM)': 'M-1.0',
        'M15': 'M-1.5',
        'M20': 'M-2.0',
        'M25': 'M-2.5',
        'O10': 'O-1.0',
        'O20(CH)': 'O-2.0',
        'O-2.0(CH)': 'O-2.0',
        'S-7': 'S-7',
        'S10': 'S-10',
        'S15': 'S-15',
        'S25': 'S-25',
        'S40': 'S-40',
        'SC10': 'SC-10',
        'SC7': 'SC-7',
        'T-5': 'T-5',
        'T-6': 'T-6'
    }

def convert_zone(zone):

    return zone_map.get(zone, zone)
   




def simple_size(num):
    if num > 10000:
        return "%sk" % int(num/1000) 
    else:
        return "%i" % num

def short_price(price):
    if price > 1e7:
        return "$%sM" % int(price/1e6)
    elif price > 1e6:
        return "$%.1fM" % (float(price)/1e6)
    elif price > 1000:
        return "$%sK" % int(price/1e3)
    else:
        return "$%s" % int(price)

def guess_units(row):
    return int(row['units'])
    if row['type'] == "TWO-FAM-RES":
        return 2
    if row['property_class'] == 'SNGL-FAM-RES':
        return 1
    if row['property_class'] == "CONDO-BLDG":
        return int(row['props_in_lot']) - int(row['buildings'])

    else:
        return int(row['units'])

def guess_lot_size(row):
    lot_size, gis_lot_size = float(row.get('area', 0) or 0), float(row.get('gis_area', 0) or 0)
    return lot_size or gis_lot_size

def conforming(row):
    far = {
        'S-40': 0.15,
        'S-25': 0.20,
        'S-15': 0.25,
        'S-10': 0.30,
        'S-7': 0.35,
        'S-0.5P': .25, # multi-family, 0.50
        'S-0.75P': 0.35, # multi-family 0.75
        'SC-7': 0.35,
        'SC-10': 0.35,
        'S-4': 1.0,
        'T-6': 0.75,
        'T-5': 1.0,
        'F-1.0': 1.0,
        'M-0.5': 0.5,
        'M-1.0': 1.0, # 1.3 attached
        'M-1.5': 1.5,
        'M-2.0': 2.0,
        'M-2.5': 2.5,
        'L-0.5': 0.5,
        'L-1.0': 1.0,
        'G-1.0': 1.0,
        # G-DP: ?
        'G-1.75': 1.75,
        'G-1.75 (LSH)': 3.30,
        'G-2.0': 2.0,
        'GMR-2.0': 2.0, # 3.45 special district
        'O-1.0': 1.0,
        'O-2.0': 2.0,
        'I-1.0': 1.0,
    }

    lot_area = {
        'S-40': {'other': 40000},
        'S-25': {'other': 25000},
        'S-15': {'other': 15000},
        'S-10': {'other': 10000},
        'S-7': {'other': 7000},
        'S-0.5P': {'1F': 15000, 'MF': (300000, 1000), 'other': 15000}, # multi-family, 0.50
        'S-0.75P': {'1F': 7000, 'MF': (140000, 1000), 'other': 7000}, # multi-family 0.75
        'SC-7': {'other': 7000},
        'SC-10': {'other': 10000},
        'S-4': {'other': 4000},
        'T-6': {'1F': 5000, '2F': 6000, '1FA': 3000, 'other': 6000},
        'T-5': {'1F': 4000, '2F': 5000, '1FA': 2500, 'other': 5000},
        'F-1.0': {'1F': 4000, '2F': 5000, '1FA': 2500, '3F': 5000, 'other': 5000},
        'M-0.5': {'1F': 4000, '2F': 5000, 'MF': (3000, 2000), 'other': 5000},
        'M-1.0': {'1F': 4000, '1FA': 2250, '2F': 5000, 'MF': (3000, 1000), 'other': 5000},
        'M-1.5': {'1F': 4000, '2F': 5000, '1FA': None, 'MF': None, 'other': 5000},
        'M-2.0': {'1F': 4000, '2F': 5000, '1FA': None, 'MF': None, 'other': 5000},
        'M-2.5': {'1F': 4000, '2F': 5000, '1FA': None, 'MF': None, 'other': 5000},
        }
    type_map = {
        'SINGLE FAMILY': '1F', 
        'TWO FAMILY': '2F', 
        'CONDO': 'MF',
        'APT 4-8 UNIT': 'MF',
        'APT 9+ UNIT': 'MF',
        }    
        
    openspace = {}

    use = {
        'S-40': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-25': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-15': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-10': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-7': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-0.5P': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'S-0.75P': ['SINGLE FAMILY', 'RELIGIOUS', 'PSCHOOL'],
        'SC-7': ['SINGLE FAMILY',' TWO FAMILY', 'CONDO', 'RELIGIOUS', 'PSCHOOL'],
        'SC-10': ['SINGLE FAMILY',' TWO FAMILY', 'CONDO', 'RELIGIOUS', 'PSCHOOL'],
    }
    exempt_use = ['RELIGIOUS', 'PSCHOOL', 'COMM MASS', 'VACANT LAND', 'TOWN OWNED', 'RES-UNDEV']

    heights = {
        'S-40': 35,
        'S-25': 35,
        'S-15': 35,
        'S-10': 35,
        'S-7': 35,
        'S-0.5P': 35,
        'S-0.75P': 35,
        'SC-7': 35,
        'SC-10': 35,
        'S-4': 35,
        'T-6': 35,
        'T-5': 35,
        'F-1.0': 40,
        'M-0.5': 35,
        'M-1.0': 40, # 1.3 attached
        'M-1.5': 50,
        'M-2.0': 50,
        'M-2.5': 50,
        'L-0.5': 40,
        'L-1.0': 40,
        'G-1.0': 40,
        # G-DP: ?
        'G-1.75': 45,
        'G-1.75 (LSH)': 90,
        'G-2.0': 45,
        'GMR-2.0': 115, # 3.45 special district
        'O-1.0': 40,
        'O-2.0': 50,
        'I-1.0': 110,
    }
    lot_size = guess_lot_size(row)

    zone = convert_zone(row['zoning'])

    units = guess_units(row)
    non_conforming = []

    if row['living_area'] and lot_size and zone in far:
        prop_far = float(row['living_area']) / float(lot_size)
        if prop_far > far[zone]:
            non_conforming.append("density")
    if zone in lot_area:
        req = None
        c = lot_area[zone]
        t = type_map.get(row['type'], 'other')
        if row['attached']:
            t = '1FA'
        if t in c:
            req = c[t]
        else:
            req = c['other']
        if type(req) == type(()):
            req = req[0] + req[1]*(units-1)
        if req != None and lot_size < req and row['type_code'] != "132":
            non_conforming.append('lot size')
    if zone in use:
        if row['type'] not in exempt_use and row['type'] not in use[zone]:
            non_conforming.append('property type')
    if row['height'] and zone in heights and row['height'] > heights[zone] * 1.2:
        non_conforming.append("height")
    if row['setback_problem']:
        non_conforming.append('setbacks')
    if non_conforming:
        return "Non-conforming (%s)." % (", ".join(non_conforming))
    return ""

def approx_height(row):
    height_approx = 0
    if row['story_height']:
        height_approx = int(float(row['num_stories']) * int(row['story_height']))
        if row['height']:
            height = float(row['height'])
            if height/height_approx > 4 or height/height_approx < .4:
                return -1
    return height_approx

def write_row(row):
    text = []
    zone = row.get('zone', '')
    addr = row['address'].title()
    text.append("%s -" % addr)
    if row['type'] in class_lookup:
        if row['type'] == 'SINGLE FAMILY' and row['bedrooms']:
            text.append("%s bedroom single family home." % (row['bedrooms']))
        else: 
            text.append("%s." % class_lookup[row['type']])
    else:
        text.append("%s." % row['type'].title())
    if row['year_built'] and int(row['year_built']) != 0:
        text.append("Built %s." % (row['year_built']))
    if row['units'] > 1 and row['type'] not in ["TWO FAMILY", "THREE FAMILY"]:
        text.append("%s units." % row['units'])
    if row['living_area']:
        text.append("%s sqft." % simple_size(int(row['living_area'])))
    text.append("%s zone." % row['zoning'])
    lot_size = guess_lot_size(row)
    if lot_size:
        text.append("%s sqft lot." % simple_size(lot_size))
    if row['sale_date'] and row['sale_date'] != "12/31/1899" and row['sale_price'] and int(row['sale_price']) > 10000:
        text.append("Last sold: %s, %s." % (row['sale_date'], short_price(int(row['sale_price']))))
    elif row['year_sold'] and row['type'] == 'CONDO':
        text.append("A unit last sold in %s." % row['year_sold'])
    if row['parking_spaces'] > 0:
        text.append("%s parking spaces." % row['parking_spaces'])
    if int(row['assessment']):  
        text.append("Current assessment: %s. 2020 taxes: %s." % (short_price(int(row['assessment'])), short_price(row['tax'])) )
    conf = conforming(row)
    if conf:
        text.append(conf)
    gmaps_link = "https://www.google.com/maps/search/?api=1&query=%s" % urllib.quote("%s, Brookline, MA" % addr)
    text.append(gmaps_link)
    my_lookup = "https://crschmidt.net/housing/brookline/proplookup?pid=%s&use=%s" % (row['pid'], row['type_code'])
    text.append(my_lookup)    
    t = " ".join(text)
    #while len(t) > 238 + len(gmaps_link) + len(my_lookup): # Hack for entries which are too long.
    #    print t
    #    text.pop(-4)
    #    t = " ".join(text)   
    return t


def output_html(row):
    text = write_row(row)
    output = """<tr valign="top">
   <td>%s</td>
   <td>%s</td>
   <td><img src="https://housing.crschmidt.net/brookline-gis/%s.png" height="256px" /></td>
   <td><img src="https://housing.crschmidt.net/brookline-images/%s.jpg" height="256px" /></td>
   </tr>""" % (row['address'], text, row['gisid'], row['pid'])
    return output
   
def output_conformance(row):
    out = "0"
    if len(conforming(row)) > 0:
        out = "1"
    return ",".join([row['gisid'], out]) 

if __name__ == "__main__":
    conn = sqlite3.connect("../data/brookline.db")
    
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    c = conn.cursor()
    c.row_factory = dict_factory
    m = 0
    for row in c.execute("SELECT * FROM lots"):
        t = write_row(row)
        if len(t)>m:
            m = len(t)
        if True: # len(t) > 380: 
            print(t)    
            pass
