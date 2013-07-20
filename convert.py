# Convert DC building footprints and addresses into importable chunks of OSM files.
# Not done folks.

import subprocess
from fiona import collection
from pprint import pprint
from lxml import etree
from lxml.etree import tostring

# create XML 
results = etree.Element('osm', version='0.6', generator='alex@mapbox.com')

with collection("AddressPt/addresses.shp", "r") as input:
    for address in input:
        pprint(address)
        node = etree.Element('node',
            lat=str(address['geometry']['coordinates'][0]),
            lon=str(address['geometry']['coordinates'][0]))
        results.append(node)
        break

handle = open('buildings.osm', 'w')
handle.writelines(tostring(results, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
handle.close()

exit(0)

with collection("BldgPly/buildings.shp", "r") as input:
    for building in input:
        pprint(building)
        break

