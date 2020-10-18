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

import json
import fiona
import shapely.geometry

zone_shapes = []
zones = fiona.open("../data/src/Zoning_1598232505822.geojson")
for feature in zones:
    if feature['geometry']:
        zone_shapes.append([shapely.geometry.shape(feature['geometry']), feature])

parcels = fiona.open("../data/src/Parcels_1598231695808.geojson")
count = 0

zones = {}
for parcel in parcels:
    pid = parcel['properties']['PARCELID']
    zones[pid] = ''
    count += 1
    if count % 100 == 0: print count
    lot_base = shapely.geometry.shape(parcel['geometry'])
    o = 0
    for zone in zone_shapes:
        if lot_base.intersects(zone[0]):
            overlap = lot_base.intersection(zone[0])
            n = overlap.area / lot_base.area
            if n > o:
                zones[pid] = zone[1]['properties']['ZONECLASS']
                o = n
                
f = open("zones.csv", "w")
f.write("id,zone\n")
for i in zones:
    f.write("%s,%s\n" % (i, zones[i]))       
f.close()
