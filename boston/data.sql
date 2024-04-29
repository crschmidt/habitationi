.mode csv
.separator ','
.import fy2024-property-assessment-data_1_5_2024.csv Properties
update Properties set LAND_VALUE=REPLACE(LAND_VALUE, ',', '');
update Properties set TOTAL_VALUE=REPLACE(TOTAL_VALUE, ',', '');
update Properties set BLDG_VALUE=REPLACE(BLDG_VALUE, ',', '');
