# Convert DC building footprints and addresses into importable chunks of OSM files.

from fiona import collection
from lxml import etree
from lxml.etree import tostring
from rtree import index
from shapely.geometry import asShape
from shapely import speedups
from shapely.prepared import prep

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

del addresses

# Generate a new osmId
osmIds = dict(node = -1, way = -1, rel = -1)
def newOsmId(type):
    osmIds[type] = osmIds[type] - 1
    return osmIds[type]

# Add a building to a given OSM xml document.
# TODO:
# - Add address to building tag where only one address
def appendBuilding(building, osmXml):
    way = etree.Element('way', visible = 'true', id = str(newOsmId('way')))
    way.append(etree.Element('tag', k = 'building', v = 'yes'))
    for pos in building['geometry']['coordinates'][0]:
        id = str(newOsmId('node'))
        node = etree.Element('node',
            lon=str(pos[0]),
            lat=str(pos[1]),
            visible='true',
            id=id)
        osmXml.append(node)
        way.append(etree.Element('nd', ref=id))
    osmXml.append(way)

# Export .osm file by census tract.
# TODO:
# - Collect and export addresses where more than one address per building
with collection("TractPly/tracts.shp", "r") as input:
    for tract in input:
        # Generate XML document
        osmXml = etree.Element('osm', version='0.6', generator='alex@mapbox.com')
        for i in buildingIdx.intersection(asShape(tract['geometry']).bounds):
            appendBuilding(buildings[i], osmXml)

        # Write XML document to disc.
        handle = open(u'results/dc-%s.osm' % tract['properties']['TRACT'], 'w')
        handle.writelines(tostring(osmXml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        handle.close()
