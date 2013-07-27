# Convert DC building footprints and addresses into importable OSM files.
from fiona import collection
from lxml import etree
from lxml.etree import tostring
from rtree import index
from shapely.geometry import asShape
from shapely import speedups
from sys import argv
from glob import glob
import re
from pprint import pprint

speedups.enable()

def convert(buildingIn, addressIn, buildingOut, addressOut):
    # Load all addresses
    addresses = []
    with collection(addressIn, "r") as input:
        for address in input:
            shape = asShape(address['geometry'])
            shape.original = address
            addresses.append(shape)

    # Load and index all buildings
    buildingIdx = index.Index()
    buildings = []
    with collection(buildingIn, "r") as input:
        for building in input:
            building['shape'] = asShape(building['geometry']).simplify(0.000005, True)
            buildings.append(building)
            buildingIdx.add(len(buildings) - 1, building['shape'].bounds)

    # Map addresses to buildings
    for address in addresses:
        for i in buildingIdx.intersection(address.bounds):
            if building['shape'].contains(address):
                if not buildings[i]['properties'].has_key('addresses'):
                    buildings[i]['properties']['addresses'] = []
                buildings[i]['properties']['addresses'].append(address.original)

    del addresses

    # Generate a new osmId
    osmIds = dict(node = -1, way = -1, rel = -1)
    def newOsmId(type):
        osmIds[type] = osmIds[type] - 1
        return osmIds[type]

    # Appends an address to a given node or way.
    def appendAddress(address, element):
        if 'ADDRNUM' in address:
            element.append(etree.Element('tag', k = 'addr:housenumber', v = str(address['ADDRNUM'])))
        if all (k in address for k in ('STNAME', 'STREET_TYP', 'QUADRANT')):
            street = "%s %s %s" % \
                (address['STNAME'].title(), # TODO: turns 42nd into 42Nd
                address['STREET_TYP'].title(),
                address['QUADRANT'])
            element.append(etree.Element('tag', k = 'addr:street', v = street))

    # Appends a building to a given OSM xml document.
    def appendBuilding(building, address, osmXml):
        # Create building node
        way = etree.Element('way', visible = 'true', id = str(newOsmId('way')))
        way.append(etree.Element('tag', k = 'building', v = 'yes'))

        # Attach address to building
        if address:
            appendAddress(address['properties'], way)

        # Export building nodes
        for pos in building['shape'].exterior.coords:
            id = str(newOsmId('node'))
            node = etree.Element('node', visible='true', id= id )
            node.attrib['lon'] = str(pos[0])
            node.attrib['lat'] = str(pos[1])
            osmXml.append(node)
            way.append(etree.Element('nd', ref=id))
        osmXml.append(way)

    # Export buildings.
    addresses = []
    osmXml = etree.Element('osm', version='0.6', generator='alex@mapbox.com')
    for building in buildings:
        address = None
        # Only export address with building if exactly one address per building.
        if 'addresses' in building['properties']:
            if (len(building['properties']['addresses']) == 1):
                address = building['properties']['addresses'][0]
            else:
                addresses.extend(building['properties']['addresses'])
        appendBuilding(building, address, osmXml)

    with open(buildingOut, 'w') as outFile:
        outFile.writelines(tostring(osmXml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        print "Exported " + buildingOut

    # Export separate addresses.
    if (len(addresses) > 0):
        osmXml = etree.Element('osm', version='0.6', generator='alex@mapbox.com')
        for address in addresses:
            node = etree.Element('node', visible = 'true', id = str(newOsmId('node')))
            node.attrib['lon'] = str(address['geometry']['coordinates'][0])
            node.attrib['lat'] = str(address['geometry']['coordinates'][1])
            appendAddress(address['properties'], node)
            osmXml.append(node)
        with open(addressOut, 'w') as outFile:
            outFile.writelines(tostring(osmXml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            print "Exported " + addressOut

if (len(argv) == 2):
    convert(
        'chunks/buildings-%s.shp' % argv[1],
        'chunks/addresses-%s.shp' % argv[1],
        'osm/buildings-%s.osm' % argv[1],
        'osm/addresses-%s.osm' % argv[1])
else:
    buildingFiles = glob("shapefiles/buildings-*.shp")
    for buildingFile in buildingFiles:
        matches = re.match('^.*-(\d+)\.shp$', buildingFile).groups(0)
        convert(
            buildingFile,
            'chunks/addresses-%s.shp' % matches[0],
            'osm/buildings-%s.osm' % matches[0],
            'osm/addresses-%s.osm' % matches[0])
