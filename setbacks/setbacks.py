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

if __name__ == "__main__":
    conn = sqlite3.connect('prop.db')
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    c = conn.cursor()
    c.row_factory = dict_factory
    m = 0
    for row in c.execute("SELECT * FROM lots"):
        print ",".join([row['gisid'], str(compute_setback(row['zone'], row['height']))])
