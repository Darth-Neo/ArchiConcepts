MATCH (p:DataObject)-[r3*0..2]->(q:DataObject) where left(p.parentPath, 42) = "/CMS INTO ECM V6/Application/Content Model"
RETURN distinct p.aname, count(q) order by count(q) desc