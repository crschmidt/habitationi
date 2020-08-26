#!/bin/sh -x

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

output=brookline.db

rm *.csv
rm $output
rm -rf tmp

cat updates.sql | sqlite3 $output
ogr2ogr -append -f sqlite -nln parcels prop.db src/Parcels_1598231695808.geojson
cat data.sql | sqlite3 $output
python ../zoning/intersect_zone.py
cat load_zoning.sql | sqlite3 $output
python ../zoning/gen_setbacks.py $output
python ../parcels/centroid.py
mkdir tmp
ogr2ogr -f GeoJSON -t_srs EPSG:2249 tmp/Buildings2249.geojson src/Buildings_1598260534885.geojson
ogr2ogr -f GeoJSON -t_srs EPSG:2249 tmp/Parcels2249.geojson src/Parcels_1598231695808.geojson 
python ../buildings/building_info.py
cat load_extras.sql | sqlite3 $output
