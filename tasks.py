# Generate polygon file for tasking manager.
# import_url: "http://example.com/buildings-addresses-000100.osm"
import json
import sys

import_url_template = "http://dcbuildings.s3.amazonaws.com/buildings-addresses-%s.osm"
file_name = "BlockGroupPly/buildings.geojson"

with open(sys.argv[1]) as f:
    polys = json.load(f)
    for p in polys['features']:
        p['properties'] = {
            'TRACT': p['properties']['TRACT'],
            'import_url': import_url_template % p['properties']['TRACT']
        }
    print json.dumps(polys, indent=4)
