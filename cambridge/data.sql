DROP TABLE lots;
DROP TABLE meta_parcels;

create table lots AS select min(PID) as pid,
 GISID as gisid,
 count(PID) as props_in_lot,
 count(distinct BldgNum) as buildings,
 sum(CASE WHEN (PropertyClass =='CONDOMINIUM' or PropertyClass='CNDO LUX') THEN 1 ELSE Interior_NumUnits END) as units,
 cast(max(LandArea) as integer) as lot_size,
 sum(Interior_LivingArea) as living_size,
 sum(Interior_Bedrooms) as bedrooms,
 address_only as address,
 min(PropertyClass) as type,
 min(PropertyClass) as property_class,
 cast(sum(CASE WHEN BldgNum=='1' THEN AssessedValue ELSE 0 END) as integer) as assessed_value,
 min(cast(CASE WHEN Condition_YearBuilt != '0' THEN Condition_YearBuilt else null end as integer)) as year_built,
 max(CASE WHEN cast(SalePrice as integer) > 10000 THEN cast(substr(SALEDATE, -4) as integer) ELSE null END) as sale_year,
 SALEDATE as sale_date,
 cast(sum(CASE WHEN PropertyClass != 'CONDO-BLDG' THEN SalePrice ELSE 0 END) as integer) as sale_price,
 max(Exterior_NumStories) as num_stories,
 max(Exterior_WallHeight) as story_height,
 sum(Parking_Open)+sum(Parking_Covered)+sum(Parking_Garage) as parking_spaces,
 max(Zoning) as zone,
 null as gis_lot_size,
 null as building_area,
 null as driveway_area,
 null as open_area,
 null as height,
 null as setback,
 0 as setback_nonconf,
 '' as census,
 '' as neighborhood,
 '' as nonconf_reasons,
 0 as nonconf,
 '' as n_nonconf_reasons,
 0 as n_nonconf,
 0 as allowed_units,
 0 as byright_units,
 null as bbox
from properties 
group by GISID;

