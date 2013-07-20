#! /bin/bash

ogr2ogr -t_srs EPSG:3857 BldgPly/buildings.shp BldgPly/BldgPly.shp
ogr2ogr -t_srs EPSG:3857 AddressPt/addresses.shp AddressPt/AddressPt.shp

