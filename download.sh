#! /bin/bash
curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=1021&downloadTYPE=ESRI" -o BldgPly.zip
curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=2182&downloadTYPE=ESRI" -o AddressPt.zip
unzip BldgPly.zip -d BldgPly
unzip AddressPt.zip -d AddressPt
ogr2ogr -t_srs EPSG:4326 BldgPly/buildings.shp BldgPly/BldgPly.shp
ogr2ogr -t_srs EPSG:4326 AddressPt/addresses.shp AddressPt/AddressPt.shp
