insert into sjConfig_History (id, ParentID, Org, Object, Instance, Property, DataType, Value)
Select id, ParentID, Org, Object, Instance, Property, DataType,
'***deleted***' as Value
from sjConfig where id = 3;


select * from sjConfig where id = 3 and Value <> '***deleted***'