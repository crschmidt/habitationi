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

import json
import fiona
import shapely.geometry

property_setbacks = {}
f = open('setbacks.csv')
for line in f:
    line = line.strip()
    gisid, setback = line.split(",")
    if float(setback):
        property_setbacks[gisid] = float(setback)

driveway_shapes = []
driveways = fiona.open("BASEMAP_Buildings.shp")
for feature in driveways:
    if feature['geometry']:
        driveway_shapes.append([shapely.geometry.shape(feature['geometry']), feature])

parcels = fiona.open("ASSESSING_ParcelsFY2019.shp")
count = 0
ml = 0
for parcel in parcels:
    count += 1
    gisid = parcel['properties']['ML']
    if not gisid in property_setbacks: 
        continue 
    setback = property_setbacks[gisid]
    lot_base = shapely.geometry.shape(parcel['geometry'])
    lot = shapely.geometry.shape(parcel['geometry']).buffer(-setback)
    intersects = False
    if lot.type != "MultiPolygon":
        boundary = shapely.geometry.LineString(lot.exterior)
        for i in driveway_shapes:
            if not lot_base.intersects(i[0]):
                continue
            building_overlap = lot_base.intersection(i[0])
            if building_overlap.area > .85 * i[0].area:
                if boundary.intersects(i[0]):
                    intersects = True
    print ",".join(map(str, [gisid,setback,intersects and 1 or 0]))
print count, ml    
