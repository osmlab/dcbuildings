
wget http://download.geofabrik.de/north-america/us/district-of-columbia-latest.osm.pbf


osmosis --read-pbf district-of-columbia-latest.osm.pbf  --way-key keyList="building" --tf reject-nodes --tf reject-relations --write-xml - | python parse_buildings.py > osm-buildings.tsv


dcb <- read.delim("~/project/dcbuildings/analytics/osm-buildings.tsv")

