DC building footprint import
============================

[Work in progress.](https://github.com/osmlab/dcbuildings/issues)

Generates an OSM file of buildings with addresses per DC census tract, ready
to be used in JOSM for a manual review and upload to OpenStreetMap.

## Usage

The do-it-all-at-once way (will take upwards of 5 minutes):

    # Download all files and process them into OSM
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

    # Sometimes useful: convert only specific census tracts.
    # Convert only census tract number 2.
    python convert.py 2

## Related

- [Ongoing import proposal (not updated with this script yet)](http://www.sixpica.com/osm/2013/05/19/proposal-for-importing-dc-gis-building-data-to-osm/)
- [DC import page](http://wiki.openstreetmap.org/wiki/Washington_DC/DCGIS_imports)
