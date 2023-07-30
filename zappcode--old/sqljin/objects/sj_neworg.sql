DROP VIEW  IF EXISTS   ObjProp;
DROP VIEW  IF EXISTS   ObjProp_History;

DROP VIEW  IF EXISTS   Properties;
DROP TABLE IF EXISTS   sjProperties;

DROP VIEW  IF EXISTS   Objects;
DROP TABLE IF EXISTS   sjObjects;


CREATE TABLE IF NOT EXISTS   sjObjects
(ID           int  PRIMARY KEY
,ObjectType   text NOT NULL
,InstanceName text NOT NULL
,Active       int  default(1) NOT NULL
);

CREATE VIEW IF NOT EXISTS   Objects  as
Select * from sjObjects
where Active > 0
;



CREATE TABLE IF NOT EXISTS   sjProperties
(ID           int   NOT NULL
,PropName     text  NOT NULL
,PropValue    text default '' NOT NULL
,PropType     text default 'str'
,Sort         int  default (500)
,VarFlag      int  default (0)
,StartTS      text  DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))  NOT NULL
,PRIMARY KEY(ID, PropName, StartTS)
,FOREIGN KEY (ID) REFERENCES sjObjects
);


CREATE VIEW IF NOT EXISTS   Properties  as
Select * from sjProperties
where PropValue != '***deleted***'
  and (ID, PropName, StartTS) in 
(Select ID, PropName, max(StartTS) from sjProperties group by ID, PropName)
;



CREATE VIEW IF NOT EXISTS   ObjProp  as
Select o.ID, o.ObjectType, o.InstanceName, o.Active,
p.PropName, p.PropValue, p.PropType, p.Sort, p.VarFlag, p.StartTS      
from Objects as o
left outer join Properties as p
    on o.ID = p.ID 
;


CREATE VIEW IF NOT EXISTS   ObjProp_History  as
Select o.ID, o.ObjectType, o.InstanceName, o.Active,
p.PropName, p.PropValue, p.PropType, p.Sort, p.VarFlag, p.StartTS      
from sjObjects as o
left outer join sjProperties as p
    on o.ID = p.ID 
;

