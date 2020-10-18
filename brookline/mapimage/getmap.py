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

import sqlite3
from io import BytesIO

def get_map(gisid, bbox):
    print gisid, bbox
    data = {
            'm': 'MakeMapImage',
            'state': """{"Application":"Assessors","MapTab":"AssessorsDefault","Level":"","Action":0,"TargetLayer":"Parcels","TargetIds":[""],"ActiveMapId":"%s","ActiveDataId":"%s","Proximity":"","SelectionLayer":"","SelectionIds":[],"Query":"ParcelsQueryAll","DataTab":"ParcelsBasicInfo","MarkupCategory":"","MarkupGroups":[],"FunctionTabs":3,"ActiveFunctionTab":2,"Coordinates":[],"CoordinateLabels":[],"Extent":{"bbox":[%s]},"VisibleLayers":{"AssessorsDefault":["Zoning","StreetEdges","Buildings","Parcels","Openspace"],"AssessorsPhoto":["Photo2008","PhotoBoundary","PhotoParcels"]}}""" % (gisid, gisid, ",".join(map(str, bbox))),
            'width': 768,
            'height': 512,
        }
    print data['state']    
    import urllib
    d = urllib.urlencode(data)
    data = urllib.urlopen("https://gisweb.brooklinema.gov/gpv/Services/MapImage.ashx", d).read()
    print data
    im = BytesIO()
    im.write(urllib.urlopen("https://gisweb.brooklinema.gov/gpv/%s" % data[1:-1]).read())
    im.seek(0)
    return im

if __name__ == "__main__":
    import fiona
    import shapely.geometry
#    f = open('image.png', 'w') 
#    f.write(get_map('', '').read())
    
    parcels = fiona.open("../data/tmp/Parcels2249.geojson")
    done = 0
    for parcel in parcels:
        lot = shapely.geometry.shape(parcel['geometry'])
        lot = lot.buffer(100)
        bbox = map(int, lot.bounds)
        f = open('/mnt/airbnbdisk/crschmidt/brookline-gis/%s.png' % parcel['properties']['PARCELID'], 'w') 
        f.write(get_map(parcel['properties']['PARCEL_ID'], bbox).read())
        f.close()
        done += 1
        if done % 10 == 0: print done
