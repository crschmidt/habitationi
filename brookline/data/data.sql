DROP TABLE lots;
CREATE TABLE lots AS 
select
  MIN("PARCEL-ID") as pid, 
  substr(cmpxid, 0, length(cmpxid)-1) as gisid,
   USECD as type_code,
   DESCRIPTION as type,
   cast('f' as boolean) as attached,
   ZONING as zoning,
   ADDNO1 || ' ' || ADDST1 as address,
   cast(SUM(BEDROOMS) as integer) as bedrooms,
   CAST(sum(cast("LIVING-AREA" as integer)) as integer) as living_area,
   cast(0 as integer) as area,
   cast(CASE WHEN TOT_LND_AREA != '0.0' THEN cast(TOT_LND_AREA as float) ELSE cast("shape.starea()" as float) END as float) gis_area,
   cast(land_value as integer) as land_value, cast(bldg_value as integer) as building_value, cast(tot_value as integer) as total_value,
   cast(SUM(cast(" RESTOTLVAL " as integer)) + SUM(cast(COMTOTLVAL as integer)) + SUM(cast(" EXMTOTLVAL " as integer) ) as integer) as assessment,
   cast(SUM(cast(TOTFYTAX as float)) as float) as tax,
   cast(MIN(CAST("YEAR-BUILT" AS INTEGER)) as integer) as year_built,
   '' as sale_date,
   cast(0 as integer) as sale_price,
   cast(SUM(cast("RES-UNITS" as integer)) as integer) as units,
   cast(SUM(CAST("PARK-GARGE" as integer))+SUM(cast("PARK-COVRD" as integer))+SUM(cast("PARK-OPN" as integer)) as integer) as parking_spaces,
   COUNT(*) as properties,
   cast(max(year_sold) as integer) as year_sold
FROM
  Properties p LEFT JOIN Parcels par ON substr(p.cmpxid, 0, length(p.cmpxid)-1)=par.parcelid
WHERE
  CMPXID != ''
GROUP BY 
  CMPXID
ORDER BY "PARCEL-ID";

INSERT INTO LOTS
select
  "PARCEL-ID" as pid, 
  "PARCEL-ID" as gisid,
   USECD as type_code,
   DESCRIPTION as type,
   CASE WHEN "BLDG-STYLE-1" IN ('ROW END', 'ROW MIDDLE') THEN 't' ELSE 'f' END as attached,
   ZONING as zoning,
   ADDNO1 || ' ' || ADDST1 as address,
   cast(BEDROOMS as integer)+"BEDROOMS-1"+"BEDROOMS-2"+"BEDROOMS-3" as bedrooms,
   CAST("TOT_FIN_AREA" as integer) as living_area,
   CAST(LANDAREA AS INTEGER) as area,
   CASE WHEN TOT_LND_AREA != '0.0' THEN cast(TOT_LND_AREA as float) ELSE cast("shape.starea()" as float) END gis_area,
   cast(land_value as integer) as land_value, cast(bldg_value as integer) as building_value, cast(tot_value as integer) as total_value,
   cast(" RESTOTLVAL " as integer) + cast(COMTOTLVAL as integer) + cast(" EXMTOTLVAL " as integer)  as assessment,
   cast(TOTFYTAX as float) as tax,
   CAST("YEAR-BUILT-1" AS INTEGER) as year_built,
   saledate as sale_date,
   saleprice as sale_price,
   cast("RES-UNITS" as integer) as units,
   CAST("PARK-GARGE" as integer)+cast("PARK-COVRD" as integer)+cast("PARK-OPN" as integer) as parking_spaces,
   1 as properties,
   year_sold as year_sold
FROM
  Properties p LEFT JOIN Parcels par ON "PARCEL-ID"=par.parcelid
WHERE
  CMPXID == ''
GROUP BY 
  "PARCEL-ID"
ORDER BY "PARCEL-ID";
