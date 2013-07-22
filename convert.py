# Convert DC building footprints and addresses into importable chunks of OSM files.
# Not done folks.

import subprocess
from fiona import collection
from pprint import pprint
from lxml import etree
from lxml.etree import tostring
from rtree import index
from shapely.geometry import asShape
from shapely import speedups

speedups.enable()

# Load all addresses
addresses = []
with collection("AddressPt/addresses.shp", "r") as input:
    for address in input:
        shape = asShape(address['geometry'])
        shape.original = address
        addresses.append(shape)

# Load and index all buildings
buildingIdx = index.Index()
buildings = []
with collection("BldgPly/buildings.shp", "r") as input:
    i = 0
    for building in input:
        buildings.append(building)
        shape = asShape(building['geometry'])
        buildingIdx.add(len(buildings) - 1, shape.bounds)

# Map addresses to buildings
for address in addresses:
    for i in buildingIdx.intersection(address.bounds):
        if not buildings[i]['properties'].has_key('addresses'):
            buildings[i]['properties']['addresses'] = []
        buildings[i]['properties']['addresses'].append(address.original)

# Where there is more than one address per building
# we export them as single nodes
addresses = []
for building in buildings:
    if 'addresses' in building['properties'] and len(building['properties']['addresses']) > 2:
        addresses.extend(building['properties']['addresses'])

pprint(len(buildings))
pprint(len(addresses))

exit(0)

# TODO
#
# - discount already existing buildings and addresses
# - cut up buildings and addresses by census tracts
# - write out one .osm file per tract

# create XML 
results = etree.Element('osm', version='0.6', generator='alex@mapbox.com')

ids = dict(
    node = -1,
    way = -1,
    rel = -1
)
def newId(type):
    ids[type] = ids[type] - 1
    return ids[type]

with collection("AddressPt/addresses.shp", "r") as input:
    for address in input:
        # pprint(address)
        node = etree.Element('node',
            lon=str(address['geometry']['coordinates'][0]),
            lat=str(address['geometry']['coordinates'][1]),
            visible='true',
            id=str(newId('node')))
        node.append(etree.Element('tag',
            k='addr:housenumber',
            v=str(address['properties']['ADDRNUM'])));
        results.append(node)
        break

with collection("BldgPly/buildings.shp", "r") as input:
    for building in input:
        # pprint(building)
        way = etree.Element('way',
            visible='true',
            id=str(newId('way')))
        way.append(etree.Element('tag', k='building', v='yes'));
        for pos in building['geometry']['coordinates'][0]:
            id = str(newId('node'))
            node = etree.Element('node',
                lon=str(pos[0]),
                lat=str(pos[1]),
                visible='true',
                id=id)
            results.append(node)
            way.append(etree.Element('nd', ref=id))
        results.append(way)
        break

handle = open('buildings.osm', 'w')
handle.writelines(tostring(results, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
handle.close()

exit(0)
