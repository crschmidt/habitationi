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
from io import BytesIO

def get_map(gisid, bbox):
    data = {
            'm': 'MakeMapImage',
            'state': """{"Application":"Base","MapTab":"BasePlan","Level":"","Search":"AddressPoints","SearchCriteria":{},"Action":0,"TargetLayer":"Parcels","TargetIds":["%s"],"ActiveMapId":"%s","ActiveDataId":"","Proximity":"","SelectionLayer":"","SelectionIds":[],"Query":"All_Parcels","DataTab":"PropertyInfo","MarkupCategory":"General","MarkupGroups":[],"Markup":[],"FunctionTabs":47,"ActiveFunctionTab":0,"Extent":{"bbox":[%s]},"VisibleLayers":{"BasePlan":["Addresses","Rail","RoadCenterlineCityscale","BuildingFootprints","Parcels","PavedRoads","Bridges","UnpavedRoads","UnpavedParking","Sidewalks","Driveways","Alleys","PavedParking","PublicFootpath"],"BaseOrtho":["Parcels","RoadCenterlineLabel","RoadCenterlineCityscale"]},"VisibleTiles":{"BasePlan":[],"BaseOrtho":[]}}""" % (gisid, gisid, ",".join(map(str, bbox))),
            'width': 768,
            'height': 512,
        }
    
    import urllib
    d = urllib.urlencode(data)
    data = urllib.urlopen("https://gis.cambridgema.gov/map/Services/MapImage.ashx", d).read()
    im = BytesIO()
    im.write(urllib.urlopen("https://gis.cambridgema.gov/map/%s" % data[1:-1]).read())
    im.seek(0)
    return im

if __name__ == "__main__":
    import fiona
    import shapely.geometry
    
    parcels = fiona.open("ASSESSING_ParcelsFY2019.shp")
    done = 0
    for parcel in parcels:

        if parcel['properties']['ML'] == "---":
            done += 1
            continue
        lot = shapely.geometry.shape(parcel['geometry'])
        lot = lot.buffer(100)
        bbox = map(int, lot.bounds)
        get_map(parcel['properties']['ML'], bbox)
        done += 1
        if done % 10 == 0: print done
