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
import sys

from writeup import convert_zone 

def setback_row(row):
    setback = {
        'S-40': 20,
        'S-25': 20,
        'S-15': 15,
        'S-10': 10,
        'S-7': 7.5,
        'S-0.5P': 15,
        'S-0.75P': 7.5, 
        'SC-7': 7.5,
        'SC-10': 7.5,
        'S-4': 7.5,
        'T-6': 7.5,
        'T-5': 7.5,
        'F-1.0': 7.5,
        'M-0.5': 7.5,
        'M-1.0': 7.5, 
        'M-1.5': 7.5,
        'M-2.0': 7.5,
        'M-2.5': 7.5,
    } 

    z = convert_zone(row['zoning'])
    if z in setback:
        return ",".join([row['gisid'],str(setback[z])])

if __name__ == "__main__":
    conn = sqlite3.connect(sys.argv[1])
    
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    c = conn.cursor()
    c.row_factory = dict_factory
    m = 0
    f = open("setbacks.csv", "w")
    for row in c.execute("SELECT * FROM lots"):
        sb = setback_row(row)
        if sb:
            f.write("%s\n" % sb)
