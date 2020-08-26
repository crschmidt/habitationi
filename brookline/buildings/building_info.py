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

setbacks = {}
for line in open("../data/setbacks.csv"):
    pid, setback = line.strip().split(",")
    setback = float(setback)
    setbacks[pid] = setback

building_shapes = []
buildings = fiona.open("../data/tmp/Buildings2249.geojson")
for feature in buildings:
    if feature['geometry']:
        building_shapes.append([shapely.geometry.shape(feature['geometry']), feature])

parcels = fiona.open("../data/tmp/Parcels2249.geojson")
count = 0

heights = {}
intersects = {}
for parcel in parcels:
    pid = parcel['properties']['PARCELID']
    intersects[pid] = 0
    if pid in setbacks:
        setback = setbacks[pid]
    else:
        setback = 0 
    count += 1
    if count % 100 == 0: print count
    lot_base = shapely.geometry.shape(parcel['geometry'])
    if setback:
        setback_lot = lot = shapely.geometry.shape(parcel['geometry']).buffer(-setback)
    for building in building_shapes:
        if lot_base.intersects(building[0]):
            overlap = lot_base.intersection(building[0])
            if overlap.area > .85 * building[0].area:
                if building[1]['properties']['BLDGHEIGHT'] and float(building[1]['properties']['BLDGHEIGHT']):
                    h = float(building[1]['properties']['BLDGHEIGHT'])
                    if pid not in heights:
                        heights[pid] = h
                    elif h > heights[pid]:
                        heights[pid] = h 
                if setback and setback_lot.type != "MultiPolygon":
                    boundary = shapely.geometry.LineString(setback_lot.exterior)
                    if boundary.intersects(building[0]):
                        intersects[pid] = 1
f = open("heights.csv", "w")
f.write("id,height\n")
for i in heights:
    f.write("%s,%s\n" % (i, heights[i]))       
f.close()
f = open('setback_problems.csv', 'w') 
f.write("id,problem\n")
for i in intersects:
    f.write('%s,%s\n' % (i, intersects[i]))
f.close()             
