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

import sqlite3

residential_classes = [
        'SNGL-FAM-RES',
        'TWO-FAM-RES',
        'CONDO-BLDG',
        '>8-UNIT-APT',
        'THREE-FM-RES',
        '4-8-UNIT-APT',
        'MULTIUSE-RES',
        'SINGLE FAM W/AUXILIARY APT',
        'MULTIPLE-RES',
        'MULT-RES-4-8-APT',
    ]
commercial_classes = [
        'RETAIL-STORE',
        'GEN-OFFICE',
        'RETAIL-OFFIC',
        'WAREHOUSE',
        'EATING-ESTBL',
        'INV-OFFICE',
        'HIGH-TECH',
        'GAS-STATION',
        'AUTO-REPAIR',
        'MULTIUSE-COM',
    ]

special_zones = {
        'PUD-1': 'Charles Square special development zone (near Harvard)',
        'PUD-2': 'East Cambridge Riverfront special development zone',
        'PUD-5': 'MIT @ Kendall Square special development zone',
        'PUD-6': 'North Point special development zone',
        'PUD-7': 'Volpe Center special development zone',
        }
for i in ['PUD-KS', 'PUD-3', 'PUD-3A']:
    special_zones[i] = 'Kendall Square special development zone'
for i in ['PUD-4', 'PUD-4A', 'PUD-4B', 'PUD-4C', 'PUD-4B-BA', 'PUD-4B-IA1']:
    special_zones[i] = 'East Cambridge special development zone (1st + Binney)'


class_lookup = {
        'SNGL-FAM-RES': "Single family home",
        'TWO-FAM-RES': "Two-family home",
        'CONDO-BLDG': "Condo building",
        '>8-UNIT-APT': 'Large apartment building',
        'THREE-FM-RES': 'Multi-family home',
        '4-8-UNIT-APT': 'Apartment building',
        'MULTIUSE-RES': 'Multi-use residential',
        'SINGLE FAM W/AUXILIARY APT': 'Single family home+apartment',
        'RETAIL-STORE': 'Retail store',
        'GEN-OFFICE': 'Office space',
        'Vacant City': 'Vacant city property',
        'MULTIPLE-RES': 'Multi-family residence',
        'MULTIUSE-COM': 'Multi-use commercial',
        'Church': 'Church',
        'RETAIL-OFFIC': 'Retail space',
        'PARKING-LOT': 'Parking lot',
        'RES-UDV-LAND': 'Empty lot',
        'RES-DEV-LAND': 'Empty lot',
        'WAREHOUSE': 'Warehouse',
        'EATING-ESTBL': 'Eating establishment',
        'HIGH-TECH': 'High tech',
        'INV-OFFICE': 'Office space',
        'DCR- State Parks and Rec': 'State park',
        'Vacant (Private Ed)': 'Vacant lot',
        'Vacnt Transport Authorit': 'Vacant MBTA',
        'Improved City': 'City lot',
        'COM-DEV-LAND': 'Developed lot',
        'Private College, University': 'Private College',
        'RES-UDV-PARK LND': 'Private park',
        'MULT-RES-4-8-APT': 'Apartment building',
#        RES-&-DEV-FC
#        Rectory, Parsonage
        'GAS-STATION': 'Gas Station',
        'PUB UTIL REG': 'Utility',
        'AUTO-REPAIR': 'Auto Repair',
        'CNDO LUX': 'Luxury Condo',
        'HOTEL': 'Hotel',
        'BOARDING-HSE': 'Boarding house',
        'COM-UDV-LAND': 'Empty lot',
#        Improved Local Edu
#        CONDOMINIUM
#        FRAT-ORGANIZ
#        MANUFACTURNG
#121 Corporation
#COM-PDV-LAND
#CLEAN-MANUF
#Vacant Local Education
        'BANK': 'Bank',
#Improved Public Safety
#MULT-RES-2FAM
'PARKING-GAR': 'Parking Garage',
#CNDO-RES-PKG
#MEDICAL-OFFC
#MULT-RES-1FAM
#SH-CNTR/MALL
#CHILD-CARE
#RES-LAND-IMP
#US Government
#FRAT-SORORTY
#MULT-RES->8 APT
#MULT-RES-3FAM
#Other
#Private Elementary Education
#RES LND-IMP UNDEV
#RES-PDV-LAND
#ASSISTED-LIV
#DORM-RS-HALL
#Private Secondary Education
#SUPERMARKET
#Transportation Authority
#Vacant, Tax Title
#AUTO-SALES
#INN-RESORT
#Imprvd County Admin
#MXD RETAIL-STORE
#Other- Scientific
#RES LND-IMP PT DEV
#TELE-EXCH-STA
#Utility Authority
#ELECT-PLANT
#Hospitals
#IND-DEV-LAND
#MULTIUSE-IND
#MXD 4-8-UNIT-APT
#THEATRE
#Vacant Utility Authority
#AUTO-SUPPLY
#BILLBOARD
#Cemeteries
#ELEC GEN PLANT
#GAS-CONTROL
#IND-UDV-LAND
#INDUST-CONDO
#MXD GEN-OFFICE
#NURSING-HOME
#Other Charitable
#Other Educational
#Other Open Space
#TENNIS-CLUB
#Vacant Housing Authority
}

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
    elif price > 10000:
        return "$%sK" % int(price/1e3)

def guess_units(row):
    if row['property_class'] == "TWO-FAM-RES":
        return 2
    if row['property_class'] == 'SNGL-FAM-RES':
        return 1
    if row['property_class'] == "CONDO-BLDG":
        return int(row['props_in_lot']) - int(row['buildings'])

    else:
        return int(row['units'])

def guess_lot_size(row):
    if row['gis_lot_size'] and row['property_class'] == "CONDO-BLDG":
        return float(row['gis_lot_size'])
    if row['lot_size'] and row['property_class'] != "CONDO-BLDG":
        return float(row['lot_size'])
    return 0

def conforming(row):
    types = {
            'A-1': ["SNGL-FAM-RES",'SINGLE FAM W/AUXILIARY APT'],
            'A-2': ["SNGL-FAM-RES",'SINGLE FAM W/AUXILIARY APT'],
            'B': ["SNGL-FAM-RES",'SINGLE FAM W/AUXILIARY APT', 'TWO-FAM-RES', 'CONDO-BLDG'],
    }
    for i in ['C-1', 'C-1A', 'C-2', 'C-2A', 'C-2B', 'C-3', 'C-3A', 'C-3B', 'C']:
        types[i] = residential_classes
        
    far = {
            'C': .6,
            'C-1': .75,
            'A-1': .5,
            'A-2': .5,
            'B': .5,
            'C-2': 1.75,
            'C-1A': 1.25,
            'C-2A': 2.50,
            'C-2B': 1.75,
            'C-3': 3.0,
            'C-3A': 3.0,
            'C-3B': 3.0,
            'BA': 1.75,
            'BA-1': 1.0,
            'BA-2': 1.75,
            'BA-3': 0.75,
            'BB': 3.0,
            'BB-1': 3.25,
            'BB-2': 3.0,
            'BC': 2.0,
            'BC-1': 3.0,
            'IA-1': 1.5,
            'IA-2': 4.0,
            'IA': 1.5,
            'IB-1': 3.0,
            'IB-2': 0.75,
            'O-1': .75,
            'O-2': 2.0,
            'O-2A': 1.5,
            'O-3': 3.0,
            '0-3A': 3.0,
            }
    lot_area = {
            'C': 1800,
            'C-1': 1500,
            'A-1': 6000,
            'A-2': 4500,
            'B': 2500,
            'C-2': 600,
            'C-1A': 1000,
            'C-2A': 300,
            'C-2B': 600,
            'C-3': 300,
            'C-3A': 300,
            'C-3B': 300,
            'BA': 600,
            'BA-1': 1200,
            'BA-2': 600,
            'BA-3': 1500,
            'BB': 300,
            'BB-1': 300,
            'BB-2': 300,
            'BC': 500,
            'BC-1': 450,
            'IA-1': 700,
            'IB-2': 1200,
        }
    openspace = {
            'A-1': .5,
            'A-2': .5,
            'B': .4,
            'C': .36,
            'C-1': .3,
            'C-1A': .15,
            'C-2': .15,
            'C-2B': .15,
            'C-3': .1,
            'C-3A': .1,
            'C-3B': .1,
            'O-1': .15,
            'O-2': .15,
            'O-2A': .15,
            'O-3': .1,
            'O-3A': .1,
            'BA-3': .3,
            'BB-1': .15,
            'BB-2': .15,
            'IB-2': .15,
    }
    heights = {}
    for i in ['A-1', 'A-2', 'B', 'C', 'C-1', 'O-1', 'BA-1', 'BA-3', 'IB-2', 'OS']:
        heights[i] = 35
    for i in ['C-1A', 'C-2B', 'BA-2', 'BB-2', 'IA-1', 'IC']:
        heights[i] = 45
    heights['C-2A'] = 60
    heights['C-2'] = 85
    for i in ['C-3', 'C-3A', 'C-3B', 'O-3', 'O-3A', 'IB']:
        heights[i] = 120

    lot_size = guess_lot_size(row)

    zone = row['zone']

    units = guess_units(row)
    non_conforming = []

    

    if row['living_size'] and lot_size and zone in far:
        prop_far = float(row['living_size']) / float(lot_size)
        if prop_far > far[zone]:
            non_conforming.append("density")
    if row['property_class'] in residential_classes and int(row['parking_spaces']):
        if units > int(row['parking_spaces']):
            non_conforming.append("parking")
    if lot_size and zone in lot_area and units:
        sf_unit = float(lot_size) / units
        if  sf_unit < lot_area[zone]:
            non_conforming.append("lot size/unit")
    if row['height'] and zone in heights and row['height'] > heights[zone] * 1.2:
        non_conforming.append("height")
    if lot_size and row['building_area']:
        non_open = float(row['building_area'])
        if row['driveway_area']:
            non_open += (row['driveway_area'])
        open_ratio = 1 - non_open/lot_size   
        if zone in openspace and openspace[zone] > open_ratio:
            non_conforming.append("open space")
    if row['setback_problem']:
        non_conforming.append('setbacks')
    if zone in types:
        if row['property_class'] not in types[zone] and (row['property_class'] in residential_classes or row['property_class'] in commercial_classes):
            if len(non_conforming) > 3:
                non_conforming.append("type")
            else:
                non_conforming.append("property type")
    if non_conforming:
        return "Non-conforming (%s)." % (", ".join(non_conforming))
    return ""

def write_row(row):
    text = []
    zone = row.get('zone', '')
    single_building = int(row['buildings']) == 1 and int(row['props_in_lot']) == 1
    text.append("%s -" % row['address'])
    if row['property_class'] in class_lookup:
        if row['property_class'] == 'SNGL-FAM-RES' and row['bedrooms']:
            text.append("%s bedroom single family home." % (row['bedrooms']))
        else: 
            text.append("%s." % class_lookup[row['property_class']])
    if row['year_built'] and int(row['year_built']) != 0:
        text.append("Built %s." % (row['year_built']))
    if single_building and row['num_stories'] and float(row['num_stories']):
        story_text = "%s stories" % row['num_stories']
        if float(row['num_stories']) == 1:
            story_text = "1 story"

        if row['story_height']:
            text.append("%s; ~%s ft tall." % (story_text, int(float(row['num_stories']) * int(row['story_height']))))
        else:
            text.append("%s." % story_text) 
    if single_building and row['units'] >= 3:
        text.append("%s units." % row['units'])
    if single_building and row['living_size']:
        text.append("%s sqft." % simple_size(int(row['living_size'])))
    lot_size = guess_lot_size(row)
    if lot_size:
        if row['driveway_area'] and int(row['driveway_area']) > 10:
            text.append("%s sqft lot (%s sf driveway)." % (simple_size(lot_size), simple_size(int(row['driveway_area']))))
        else:
            text.append("%s sqft lot." % simple_size(lot_size))
    if not single_building:
        if int(row['buildings']) > 1:
            text.append("%s buildings." % row['buildings'])
        if int(row['props_in_lot']) > 1:
            props = int(row['props_in_lot'])
            if row['property_class'] == "CONDO-BLDG" and props > int(row['buildings']):
                props = props - int(row['buildings'])
            text.append("%s properties." % props)
    if single_building and row['sale_date'] != "12/31/1899" and int(row['sale_price']) > 10000:
        text.append("Last sold: %s, %s." % (row['sale_date'], short_price(int(row['sale_price']))))
    if int(row['assessed_value']):    
        text.append("Current assessment: %s." % (short_price(int(row['assessed_value'])))) 
    conforms = conforming(row)    
    if conforms:
        text.append(conforms)
    if zone in special_zones:
        text.append("%s." % (special_zones[zone]))
    #text.append(row['prop_id'])
    text.append("https://www.cambridgema.gov/propertydatabase/%s" % row['prop_id'])    
    #print " ".join(text)   
    t = " ".join(text)
    while len(t) > 306: # Hack for entries which are too long.
        text.pop(-3)
        t = " ".join(text)   
    return t
    


if __name__ == "__main__":
    conn = sqlite3.connect("prop.db")
    
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
        if True: #len(t) > 306: 
            print(t)    
    print m
