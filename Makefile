all: BldgPly/buildings.shp AddressPt/addresses.shp BlockGroupPly/blockgroups.shp directories chunks osm

clean:
	rm -f BldgPly.zip
	rm -f AddressPt.zip
	rm -f BlockGroupPly.zip

BldgPly.zip:
	curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=1021&downloadTYPE=ESRI" -o BldgPly.zip

AddressPt.zip:
	curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=2182&downloadTYPE=ESRI" -o AddressPt.zip

BlockGroupPly.zip:
	curl -L "http://dcatlas.dcgis.dc.gov/catalog/download.asp?downloadID=1371&downloadTYPE=ESRI" -o BlockGroupPly.zip

BldgPly: BldgPly.zip
	rm -rf BldgPly
	unzip BldgPly.zip -d BldgPly
	rm BldgPly.zip

AddressPt: AddressPt.zip
	rm -rf AddressPt
	unzip AddressPt.zip -d AddressPt
	rm AddressPt.zip

BlockGroupPly: BlockGroupPly.zip
	rm -rf BlockGroupPly
	unzip BlockGroupPly.zip -d BlockGroupPly
	rm BlockGroupPly.zip

BldgPly/buildings.shp: BldgPly
	rm -f BldgPly/buildings.*
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite BldgPly/buildings.shp BldgPly/BldgPly.shp

AddressPt/addresses.shp: AddressPt
	rm -f AddressPt/addresses.*
	ogr2ogr -t_srs EPSG:4326 -overwrite AddressPt/addresses.shp AddressPt/AddressPt.shp

BlockGroupPly/blockgroups.shp: BlockGroupPly
	rm -f BlockGroupPly/blockgroups.*
	ogr2ogr -t_srs EPSG:4326 BlockGroupPly/blockgroups.shp BlockGroupPly/BlockGroupPly.shp

BlockGroupPly/blockgroups.geojson: BlockGroupPly
	rm -f BlockGroupPly/blockgroups.geojson
	ogr2ogr -simplify 3 -t_srs EPSG:900913 -f "GeoJSON" BlockGroupPly/blockgroups.geojson BlockGroupPly/BlockGroupPly.shp
	python tasks.py BlockGroupPly/blockgroups.geojson > BlockGroupPly/blockgroups-tasking.geojson

chunks: directories
	rm -f chunks/*
	python chunk.py AddressPt/addresses.shp BlockGroupPly/blockgroups.shp chunks/addresses-%s.shp OBJECTID
	python chunk.py BldgPly/buildings.shp BlockGroupPly/blockgroups.shp chunks/buildings-%s.shp OBJECTID

osm: directories
	rm -f osm/*
	python convert.py

directories:
	mkdir -p chunks
	mkdir -p osm
