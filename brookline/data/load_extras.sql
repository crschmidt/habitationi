alter table lots add column height float default 0;
alter table lots add column setback_problem bool default 'f';
alter table lots add column lat float;
alter table lots add column lon float;
.separator ','
.import 'setback_problems.csv' setback_problems
.import 'centroid.csv' centroids
.import 'heights.csv' heights
update lots set setback_problem=(select problem from setback_problems where id=gisid);
update lots set height=(select height from heights where id=gisid);
update lots set lat=(select lat from centroids where id=gisid);
update lots set lon=(select lon from centroids where id=gisid);
alter table lots add column random;
update lots set random=random();
