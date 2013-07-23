DC building footprint import
============================

[Work in progress.](https://github.com/osmlab/dcbuildings/issues)

Generates an OSM file of buildings with addresses per DC census tract, ready
to be used in JOSM for a manual review and upload to OpenStreetMap.

## Usage

    # Download and expand all files, reproject
    make

    # Generate importable .osm files
    # This will populate the results/ directory with one .osm file per
    # DC census tract.
    python convert.py

## Related

- [Ongoing import proposal (not updated with this script yet)](http://www.sixpica.com/osm/2013/05/19/proposal-for-importing-dc-gis-building-data-to-osm/)
- [DC import page](http://wiki.openstreetmap.org/wiki/Washington_DC/DCGIS_imports)
