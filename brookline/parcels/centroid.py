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

f = open("centroid.csv", "w")
f.write("id,lat,lon\n")

zone_shapes = []
zones = fiona.open("../data/src/Parcels_1598231695808.geojson")
for feature in zones:
    if feature['geometry']:
        centroid = shapely.geometry.shape(feature['geometry']).centroid
        f.write(",".join(map(str, (feature['properties']['PARCELID'], centroid.y, centroid.x))))
        f.write("\n")
                
f.close()
