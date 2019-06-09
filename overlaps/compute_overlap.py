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


import fiona
import shapely.geometry

driveway_shapes = []
driveways = fiona.open("BASEMAP_Driveways.shp")
for feature in driveways:
    driveway_shapes.append(shapely.geometry.shape(feature['geometry']))

parcels = fiona.open("ASSESSING_ParcelsFY2019.shp")
done = 0
for parcel in parcels:
    lot = shapely.geometry.shape(parcel['geometry'])
    intersects = 0
    area = 0
    for i in driveway_shapes:
        if lot.intersects(i):
            intersects += 1
            area += lot.intersection(i).area
    if area != 0:
        pass #print ",".join(map(str, [parcel['properties']['ML'], area])) 
    done += 1
    if done % 10 == 0: print done
