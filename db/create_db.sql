-- Copyright 2019 Christopher Schmidt
-- 
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
-- 
--     http://www.apache.org/licenses/LICENSE-2.0
-- 
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--
-- Approximate steps to creating everylot property database

.mode csv
.import fy2019.csv properties

alter table properties add column random;
update properties set random=random();

.import overlap.csv as driveways

create table everylot AS select min(PID) as prop_id,
 GISID as gisid,
 count(PID) as props_in_lot,
 count(distinct BldgNum) as buildings,
 sum(Interior_NumUnits) as units,
 sum(LandArea) as lot_size,
 sum(Interior_LivingArea) as living_size,
 sum(Interior_Bedrooms) as bedrooms,
 Address as address,
 min(PropertyClass) as property_class,
 sum(AssessedValue) as assessed_value,
 min(Condition_YearBuilt) as year_built,
 min(SaleDate) as sale_date,
 sum(SalePrice) as sale_price,
 max(Exterior_NumStories) as num_stories,
 max(Exterior_WallHeight) as story_height,
 sum(Parking_Open)+sum(Parking_Covered)+sum(Parking_Garage) as parking_spaces,
 max(Zoning) as zone,
 lonlat.lon as lon,
 lonlat.lat as lat 
from properties 
  inner join lonlat on lonlat.ml=properties.gisid 
where Exterior_occupancy!='Private College' and Exterior_occupancy!='Housing'  -- These categories have broken rows in the Cambridge fy2019 property database.
group by GISID order by min(random);
