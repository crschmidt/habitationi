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

TEST_MODE=0

import sys
try:
    import fiona
    import fiona.transform
    import shapely.geometry
    import sqlite3
except Exception, E:
    print("Missing necessary import (%s); skipping additional columns for setbacks, etc." % E)
    sys.exit()

OVERLAP_THRESHOLD=0.8

zone_setback = {
        'A-1': 15,
        'A-2': 10,
        'C-1': {'height': "{h}/5", 'min': 7.5},
        'C-1A': {'height': "{h}/7", 'max': 10},
        'SD-14': {'height': "{h}/7", 'max': 10},
        'SD-8A': {'height': "{h}/7", 'max': 10},
        'BA-2': 5,
        'SD-13': 5,
}

for i in ['B', 'C', 'SD-2', 'SD-9', 'SD-10F', 'SD-10H']:
    zone_setback[i] = 7.5

for i in ['C-2', 'C-2B', 'O-1', 'O-2', 'O-2A', 'BA-3', 'SD-4', 'SD-4A', 'SD-5', 'SD-11', 'SD-12']:
    zone_setback[i] = {'height':"{h}/5"}
for i in ['C-3', 'C-3A', 'C-2A', 'O-3', 'O-3A', 'SD-6']:
    zone_setback[i] = {'height':"{h}/6"}

def compute_setback(zone, height):
    setback = 0
    i = zone
    sb = zone_setback.get(i)
    if not sb: return setback
    if type(sb) == float or type(sb) == int:
        setback = sb
    else:
        if 'height' in sb and height:
            height = float(height)
            sb_str = sb['height'].format(h=height)
            sb_height = eval(sb_str)
            if 'min' in sb and sb_height < sb['min']:
                sb_height = sb['min']
            if 'max' in sb and sb_height > sb['max']:
                sb_height = sb['max']
            setback = sb_height   
        if 'height' in sb and not height and 'min' in sb:
            setback = sb['min']
    return setback 

def min_setback(parcel, buildings, sb=None):
    test_setbacks = range(0, 100)
    if sb: test_setbacks = [sb]
    if parcel.type != "MultiPolygon" and len(buildings):
        for setback in test_setbacks:
            try:
                lot = parcel.buffer(-setback)
                if lot.area <= 0: break
                boundary = shapely.geometry.LineString(lot.exterior)
                for i in buildings:
                        if boundary.intersects(i):
                            if sb: return True
                            return setback
            except:
                pass
    if sb:
        return False
    else:
        return -1

def get_lot_allowed_setback(db, gis, height):
    r = db.execute("SELECT zone FROM lots WHERE gisid=?", [gis])
    row = r.fetchone()
    if not row:
        return None
    z = row[0]
    return compute_setback(z, height)


def main():
    db = sqlite3.connect("cambridge.db")
    building_shapes = []
    buildings = fiona.open("tmp/buildings.geojson")
    for feature in buildings:
        building_shapes.append([shapely.geometry.shape(fiona.transform.transform_geom('EPSG:4326', 'EPSG:2249', feature['geometry'])), feature['properties']])
    driveway_shapes = []
    driveways = fiona.open("tmp/driveways.geojson")
    for feature in driveways:
        driveway_shapes.append(shapely.geometry.shape(fiona.transform.transform_geom('EPSG:4326', 'EPSG:2249', feature['geometry'])))
    census_shapes = []
    census = fiona.open("tmp/census_tracts.geojson")
    for feature in census:
        census_shapes.append([shapely.geometry.shape(fiona.transform.transform_geom('EPSG:4326', 'EPSG:2249', feature['geometry'])), feature['properties']])
    neighborhood_shapes = []
    neighborhood = fiona.open("tmp/neighborhoods.geojson")
    for feature in neighborhood:
        neighborhood_shapes.append([shapely.geometry.shape(fiona.transform.transform_geom('EPSG:4326', 'EPSG:2249', feature['geometry'])), feature['properties']])
    
    parcels = fiona.open("tmp/parcels.geojson")
    done = 0
    outputs = []
    building_lot_map = {}
    for parcel in parcels:
        if parcel['properties']['ML'] == "---":
            continue
        gisid = parcel['properties']['ML']
        lot = shapely.geometry.shape(fiona.transform.transform_geom('EPSG:4326', 'EPSG:2249', parcel['geometry']))
        bbox_str = None
        try:
            bbox_str = ",".join(map(lambda x: "%i" % x, lot.bounds))
        except:
            pass
        intersects = 0
        area = 0
        driveway_area = 0
        max_height = 0
        intersect_buildings = []
        nonconf_setback = False
        for building in building_shapes:
            i, props = building
            try:
                if lot.intersects(i):
                    intersects += 1
                    intersect_area = lot.intersection(i).area
                    if props.get("BldgID"):
                        bid = props.get("BldgID")
                        if not bid in building_lot_map:
                            building_lot_map[bid] = []
                        building_lot_map[bid].append((gisid, intersect_area))

                    area += intersect_area
                    if intersect_area/i.area > OVERLAP_THRESHOLD:
                        if props['TYPE'] != 'OUTBLDG':
                            intersect_buildings.append(i)
                        if props['TOP_GL'] > max_height:
                            max_height = props['TOP_GL']
            except Exception, E:
                print "Invalid geometry on %s (%s)" % (gisid, E)
        approx_setback = min_setback(lot, intersect_buildings)
        allowed_sb = get_lot_allowed_setback(db, gisid, max_height)
        if allowed_sb:
            nonconf_setback = min_setback(lot, intersect_buildings, allowed_sb)

        for i in driveway_shapes:
            try:
                if lot.intersects(i):
                    intersects += 1
                    driveway_area += lot.intersection(i).area
            except Exception, E:
                print "Invalid geometry on %s (%s)" % (gisid, E)
        
        census = "" 
        for geom, props in census_shapes:
            try:
                if lot.intersects(geom):
                    census = props['TRACTCE20']
            except Exception, E:
                print "Invalid geometry on %s (%s)" % (gisid, E)

        neighborhood = "" 
        for geom, props in neighborhood_shapes:
            try:
                if lot.intersects(geom):
                    neighborhood = props['N_HOOD']
            except:
                print "Invalid geometry on %s" % gisid
        if area != 0:
            db.execute("UPDATE lots SET building_area=? WHERE gisid=?", (int(area), gisid))
        if driveway_area != 0:
            db.execute("UPDATE lots SET driveway_area=? WHERE gisid=?", (int(driveway_area), gisid))
        if max_height != 0:
            db.execute("UPDATE lots SET height=? WHERE gisid=?", (max_height, gisid))
        if approx_setback != -1:
            db.execute("UPDATE lots SET setback=? WHERE gisid=?", (approx_setback, gisid))
        if nonconf_setback:
            db.execute("UPDATE lots SET setback_nonconf=1 WHERE gisid=?", (gisid,))
        if census:
            db.execute("UPDATE lots SET census=? WHERE gisid=?", (census, gisid))
        if neighborhood:
            db.execute("UPDATE lots SET neighborhood=? WHERE gisid=?", (neighborhood, gisid))
        if bbox_str:
            db.execute("UPDATE lots SET bbox=? WHERE gisid=?", (bbox_str, gisid))
            

        db.execute("UPDATE lots SET gis_lot_size=? WHERE gisid=?", (int(lot.area), gisid))
        done += 1
        if done % 250 == 0: 
            db.commit()
            print done
            if TEST_MODE: break
    bldg_gisids = []
    for bldg, data in building_lot_map.items():
        if len(data) > 1:
            data.sort(key = lambda x: x[1], reverse=True) 
        bldg_gisids.append([data[0][0], bldg])
    db.executemany("UPDATE buildings SET gisid=? WHERE bldgid=?", bldg_gisids)
    db.commit()

if __name__ == "__main__":
    main()
