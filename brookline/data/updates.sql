.separator ','
.import src/fy20.csv Properties
update Properties set " RESTOTLVAL "=REPLACE(REPLACE(" RESTOTLVAL ",' ', ''), ',', '');
update Properties set " EXMTOTLVAL "=REPLACE(REPLACE(" EXMTOTLVAL ",' ', ''), ',', '');
update Properties set "COMTOTLVAL"=REPLACE(REPLACE("COMTOTLVAL",' ', ''), ',', '');
update Properties set "TOTFYTAX"=REPLACE(REPLACE("TOTFYTAX",' ', ''), ',', '');
update Properties set "SALEPRICE"=REPLACE(REPLACE("SALEPRICE",' ', ''), ',', '');
alter table Properties add column year_sold integer;
update Properties set year_sold = cast(substr(SALEDATE, -4) as integer);

UPDATE Properties SET cmpxid='209A-13-00.9' WHERE cmpxid='209A-13-0.9';
UPDATE Properties SET cmpxid='269A-33-00.9' WHERE cmpxid='269A-33-0.9';
UPDATE Properties SET cmpxid='424A-04-00.9' WHERE cmpxid='424A-04-0.9';

