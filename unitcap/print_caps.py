import sqlite3
import unit_cap

def compute_count(options = None):
    conn = sqlite3.connect("prop.db")
    if options == None:
        options = {}
    c = conn.cursor()
    c.row_factory = unit_cap.dict_factory
    m = 0
    current = 0
    l = []
    size = 0 
    for row in c.execute("SELECT * FROM lots"):
        t = unit_cap.unit_cap(row, options=options)
        if t == -1:
            continue
        if t == 1:
            print row['prop_id']
            if row['gis_lot_size']:
                size += int(row['gis_lot_size'])
    print size
compute_count()
