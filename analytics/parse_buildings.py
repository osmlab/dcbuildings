#!/usr/bin/env python 


# Parse buildings from output of osmosis and output corresponding keys
# Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0


from lxml.etree import XMLParser, parse , iterparse, tostring
p = XMLParser(huge_tree=True)
import sys
 
 
# write to disk 
fo = open("osm-buildings.tsv","w")
 
# Documentation on iterparse
# http://effbot.org/zone/element-iterparse.htm
 
context = iterparse(sys.stdin, events=("start", "end"), huge_tree=True)
context = iter(context)
event, root = context.next()
 
print "wayid\ttimestamp\tuid\tuser\tchangeset\tkey\tvalue" 
for event, elem in context:
    if event == "end" and elem.tag == "way":
        wayid = unicode(elem.get("id"))
        timestamp = unicode(elem.get("timestamp"))
        uid = unicode(elem.get("uid")) 
        user = unicode(elem.get("user"))
        changeset = unicode(elem.get("changeset"))

        td = {}
        for i in elem.findall("tag"):
            if isinstance(i.get("v"), str):
                td[i.get("k")] = unicode(i.get("v"))
            else:
                td[i.get("k")] = i.get("v")
 
       
 	for key in td.keys():
           rvals = [ wayid, timestamp, uid, user, changeset, key, td[key] ]
           outline = u"\t".join(rvals) 
           print outline.encode("utf8") 
        
        # free up memory
        root.clear()
