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
    for row in c.execute("SELECT * FROM lots"):
        row['setback_problem'] = row['setback_nonconf']
        row['property_class'] = row['type']
        conf = writeup.conforming(row, l=True)
        conform.append([row['pid'], ",".join(conf)])
    print "Updating db"
    db.executemany("UPDATE lots SET nonconf_reasons=? WHERE PID=?", conform)
    print ("Committing")
    db.commit()
    db.execute("UPDATE lots SET nonconf=1 where nonconf_reasons!=''")
    db.commit()

if __name__ == "__main__":
    main()

