DROP TABLE lots;
CREATE TABLE lots AS 
select
  "AV PID" as pid, 
  MIN(MAP||"-"||BLOCK||"-"||LOT) as gisid, 
   PCC as type_code,
   "PCC DESCRIPT" as type,
   --cast('f' as boolean) as attached,
   ZONE as zoning,
   "HOUSE NO" || ' ' || "STREET" as address,
   cast(SUM(BEDROOM) as integer) as bedrooms,
   CAST(sum(cast("LIVING AREA" as integer)) as integer) as living_area,
   cast(SQFT as integer) as area,
   --cast(CASE WHEN TOT_LND_AREA != '0.0' THEN cast(TOT_LND_AREA as float) ELSE cast("shape.starea()" as float) END as float) gis_area,
   sum(cast("LAND VAL" as integer)) as land_value, 
   sum(cast("IMPROVE VAL" as integer)) as building_value,
   cast(SUM(cast("TAX VALUE" as integer)) as integer) as assessment,
   cast(MIN(CAST("YEAR" AS INTEGER)) as integer) as year_built,
   "SALE DATE" as sale_date,
   sum(cast("SALE PRICE" as integer)) as sale_price,
   cast(SUM(cast("OCCUP" as integer)) as integer) as units,
   COUNT(*) as properties,
   max(cast(substr("SALE DATE", -4) as integer)) as year_sold
FROM
  Properties p 
WHERE
  FISCAL_YEAR=2018
GROUP BY 
  MAP, BLOCK, LOT;
