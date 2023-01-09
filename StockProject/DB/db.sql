use django;

select  * from stock_data_data;

Delete from stock_data_data where id IN (Select c1.id FROM stock_data_data as c1
INNER JOIN stock_data_data as c2 ON c1.id > c2.id AND c1.sDate = c2.sDate AND c1.sName = c2.sName);

DELETE FROM  stock_data_data
where sDate ='2022-10-5';

SELECT PLUGIN_NAME as Name, PLUGIN_VERSION as Version, PLUGIN_STATUS as Status
FROM INFORMATION_SCHEMA.PLUGINS
WHERE PLUGIN_TYPE='STORAGE ENGINE';

select PRIMARY