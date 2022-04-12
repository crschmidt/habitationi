.mode csv
.separator ','
.import tmp/assess2022.csv Properties
alter table Properties add column year_sold integer;
update Properties set year_sold = cast(substr(SALEDATE, -4) as integer);
alter table Properties add column address_only string;
update Properties SET address_only=substr(address, 0, instr(address, '
'));
alter table Buildings add column gisid string;
