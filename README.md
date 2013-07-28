DC building and address import
==============================

**[Work in progress, do not use for import yet](https://github.com/osmlab/dcbuildings/issues)**

Generates an OSM file of buildings with addresses per DC census tract, ready
to be used in JOSM for a manual review and upload to OpenStreetMap.

## Source data

- Address Points http://data.dc.gov/Metadata.aspx?id=190
- Buildings http://data.dc.gov/Metadata.aspx?id=59

## Features

- Conflates buildings and addresses
- Cleans address names
- Exports one OSM XML building file per DC census tract
- Exports OSM XML address files for addresses that pertain to buildings with
  more than one address
- Handles multipolygons
- Simplifies building shapes

## Usage

Run all stages:

    # Download all files and process them into a building
    # and an address .osm file per census tract.
    make

You can run stages separately, like so:

    # Download and expand all files, reproject
    make download

    # Chunk address and building files by census tracts
    make chunks

    # Generate importable .osm files.
    # This will populate the osm/ directory with one .osm file per
    # DC census tract.
    make osm

    # Clean up all intermediary files:
    make clean

    # For testing it's useful to convert just a single census tract.
    # For instance, convert census tract 000100:
    python convert.py 000100

## Related

- [Ongoing import proposal (not updated with this script yet)](http://www.sixpica.com/osm/2013/05/19/proposal-for-importing-dc-gis-building-data-to-osm/)
- [DC import page](http://wiki.openstreetmap.org/wiki/Washington_DC/DCGIS_imports)
