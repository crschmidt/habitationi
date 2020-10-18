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

import csv
import urllib
import BeautifulSoup

r = csv.reader(open('../data/src/fy20.csv'))
r.next()
seen = []
failed = open("failed.txt", "w")
for row in r:
    pid = row[0]
    usecd = row[1]
    block, lot, sublot = pid.split('-')
    uid = "%s-%s-%s" % (block, lot, sublot)
    try:
        d = urllib.urlencode({'BLOCK': block, 'LOT': lot, 'SUBLOT': sublot, 'USECD': usecd})   
        d = urllib.urlopen("http://apps.brooklinema.gov/assessors/propertydetails.asp", d).read()
        soup = BeautifulSoup.BeautifulSoup(d)
        img = soup.findAll("img")[1].parent['href']
        f = open("/mnt/airbnbdisk/crschmidt/brookline-images/%s.jpg" % uid, "w")

        f.write(urllib.urlopen(img).read())
        f.close()
        seen.append(uid)
    except Exception, E:
        print "Failed at loading %s" % uid, E
        failed.write("%s,%s\n" % (uid, E))
