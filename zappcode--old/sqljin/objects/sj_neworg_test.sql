
insert into sjObjects (id, ObjectType, InstanceName) 
values(1, 'Organization','Zebra');

insert into sjProperties 
(id, PropName, PropValue, PropType) values 
 (1, 'label', 'Zebra', 'str')
,(1, 'icon location',  './icon/org.png', 'url')
,(1, 'usage api', 'http://some/url', 'url')
,(1, 'local version', 'v00.01', 'version')
,(1, 'source location type', 'github', 'str')
,(1, 'source location', 'http://raw.github.com/somefile.txt', 'url');


insert into sjProperties 
(id, PropName, PropValue, PropType) values 
(1, 'local version', 'v00.02', 'version') ;

insert into sjProperties 
(id, PropName, PropValue, PropType) values 
(1, 'source location type', '***deleted***', 'url') ;

insert into sjProperties 
(id, PropName, PropValue, PropType) values 
(1, 'local version', 'v00.03', 'version') ;

insert into sjProperties 
(id, PropName, PropValue, PropType) values 
,(1, 'source location type', 'github', 'str') ;