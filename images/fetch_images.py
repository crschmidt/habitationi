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
import time
import urllib
import re

def scrape(row):
    u = urllib.urlopen("https://www.cambridgema.gov/propertydatabase/%s" % row['prop_id'])
    data = u.read()
    m = re.search(r'PropertyImageLink_0" href="/assess/PropertyDatabase/Photos/([0-9/]*.jpg)"', data, re.IGNORECASE)
    if m:
        photo_url = "https://www.cambridgema.gov/PropertyDatabase/Photos/%s" % m.group(1)
        f = open("images/%s.jpg" % row['prop_id'], "w") 
        f.write(urllib.urlopen(photo_url).read())
        return True
    return False        

if __name__ == "__main__":
    conn = sqlite3.connect("prop.db")
    
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    failed = []
    c = conn.cursor()
    c.row_factory = dict_factory
    for row in c.execute("SELECT * FROM lots"):
        success = scrape(row)
        if not success:
            failed.append(row['prop_id'])
        print("Finished %s; (Failed: %s)" % (row['id'], ", ".join(failed)))
