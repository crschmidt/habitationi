.separator ','
.import 'zones.csv' zones
update lots set zoning=(select zone from zones where id=gisid);
