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

output=cambridge.db

rm $output
rm -rf tmp

mkdir tmp
wget -O 'tmp/assess2021.csv' 'https://data.cambridgema.gov/api/views/k3sc-zkk7/rows.csv?accessType=DOWNLOAD'
wget -O 'tmp/parcels.geojson' 'https://github.com/cambridgegis/cambridgegis_data/raw/main/Assessing/FY2021/FY2021_Parcels/ASSESSING_ParcelsFY2021.geojson'
wget -O 'tmp/buildings.geojson' 'https://github.com/cambridgegis/cambridgegis_data/raw/main/Basemap/Buildings/BASEMAP_Buildings.geojson'
wget -O 'tmp/driveways.geojson' 'https://github.com/cambridgegis/cambridgegis_data/raw/main/Basemap/Driveways/BASEMAP_Driveways.geojson'
wget -O 'tmp/neighborhoods.geojson' 'https://github.com/cambridgegis/cambridgegis_data/raw/main/Boundary/CDD_Neighborhoods/BOUNDARY_CDDNeighborhoods.geojson'
wget -O 'tmp/census_tracts.geojson' 'https://github.com/cambridgegis/cambridgegis_data/raw/main/Demographics/Census_2010/2010_Tracts/DEMOGRAPHICS_Tracts2010.geojson'
ogr2ogr -append -f sqlite -nln parcels $output tmp/parcels.geojson
cat updates.sql | sqlite3 $output
cat data.sql | sqlite3 $output
python compute_overlap.py
python generate_conformance.py
cat meta.sql | sqlite3 $output
ogr2ogr -f geojson meta_parcels.geojson $output meta_parcels
