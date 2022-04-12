-- Create the table joining the parcel data with Geo data.
create table meta_buildings as select * from buildings left join lots on lots.gisid=buildings.gisid;
create table meta_parcels as select * from lots LEFT JOIN parcels on lots.gisid = parcels.ml;
INSERT INTO geometry_columns VALUES ('meta_parcels', 'GEOMETRY', 0, 2, 4326, 'WKB');
INSERT INTO geometry_columns VALUES ('meta_buildings', 'GEOMETRY', 0, 2, 4326, 'WKB');
