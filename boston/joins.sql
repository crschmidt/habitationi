alter table parcels add column value integer;
create index prop_gis_id on properties(gis_id);
create index parcels_map_par_id on parcels(map_par_id);
UPDATE parcels
SET value = (
    SELECT SUM(TOTAL_VALUE)
    FROM properties
    WHERE properties.gis_id = parcels.map_par_id
);
alter table parcels add column value_acre;
update parcels set value_acre = cast(value/(shapestare/43560) as integer);
