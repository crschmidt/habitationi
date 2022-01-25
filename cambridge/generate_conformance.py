import sys
sys.path.append("../everylot")
import writeup
import sqlite3
def main():    
    db = sqlite3.connect("cambridge.db")
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    c = db.cursor()
    c.row_factory = dict_factory
    conform = []
    lot_units = []
    for row in c.execute("SELECT * FROM lots"):
        row['setback_problem'] = row['setback_nonconf']
        row['property_class'] = row['type']
        conf = writeup.conforming(row, l=True)
        conform.append([",".join(conf), row['pid']])
        units = writeup.allowed_lot_units(row)
        lot_units.append([units, row['pid']])
        units = min(units, 9) 
        byright_units.append([units, row['pid']])
    print "Updating db"
    db.executemany("UPDATE lots SET nonconf_reasons=? WHERE PID=?", conform)
    db.executemany("UPDATE lots SET allowed_units=? WHERE PID=?", lot_units)
    db.executemany("UPDATE lots SET byright_units=? WHERE PID=?", lot_units)
    print ("Committing")
    db.commit()
    db.execute("UPDATE lots SET nonconf=1 where nonconf_reasons!=''")
    db.commit()
    conform = []
    for row in c.execute("SELECT * FROM lots"):
        row['property_class'] = row['type']
        if row['zone'] in ['A-1', 'A-2', 'B', 'C', 'C-1']:
            row['zone'] = 'N'
        if row['zone'] == 'N' and row['setback_nonconf']==1 and row['setback'] > 5:
            row['setback_nonconf'] = 0
        row['setback_problem'] = row['setback_nonconf']
        conf = writeup.conforming(row, l=True)
        conform.append([",".join(conf), row['pid']])
    print "Updating db"
    db.executemany("UPDATE lots SET n_nonconf_reasons=? WHERE PID=?", conform)
    print ("Committing")
    db.commit()
    db.execute("UPDATE lots SET n_nonconf=1 where n_nonconf_reasons!=''")
    db.commit()



if __name__ == "__main__":
    main()

