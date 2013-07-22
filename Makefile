all: BldgPly/buildings.shp AddressPt/addresses.shp

BldgPly.zip:
	curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=1021&downloadTYPE=ESRI" -o BldgPly.zip

AddressPt.zip:
	curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=2182&downloadTYPE=ESRI" -o AddressPt.zip

BldgPly: BldgPly.zip
	unzip BldgPly.zip -d BldgPly

AddressPt: AddressPt.zip
	unzip AddressPt.zip -d AddressPt

BldgPly/buildings.shp: BldgPly
	ogr2ogr -t_srs EPSG:4326 BldgPly/buildings.shp BldgPly/BldgPly.shp

AddressPt/addresses.shp: AddressPt
	ogr2ogr -t_srs EPSG:4326 AddressPt/addresses.shp AddressPt/AddressPt.shp
