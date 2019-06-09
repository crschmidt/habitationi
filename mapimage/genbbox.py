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

import csv

parcels = fiona.open("ASSESSING_ParcelsFY2019.shp")
done = 0
w = csv.writer(open("parcelbbox.csv", "w"), "excel-tab")
for parcel in parcels:
    lot = shapely.geometry.shape(parcel['geometry'])
    lot = lot.buffer(100)
    w.writerow([parcel['properties']['ML'], ",".join(map(lambda x: "%i" % x, lot.bounds))])
