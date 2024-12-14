# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:22:57 2024
ESRI map viewer does not offer data download
	example URL
	https://www.arcgis.com/apps/mapviewer/index.html?webmap=c2e09ff2c4d04904a382771c996b25ec
using the same key with rest service URL returns JSON file
	https://www.arcgis.com/sharing/rest/content/items/c2e09ff2c4d04904a382771c996b25ec/data?f=json
this contains all of the data but it is not GeoJSON. At least QGIS does not recognise it.
This script converts it to ESRI shapeFile.
"""

import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,MultiLineString
from os.path import join as opj

outFileName='transp'

with open('data.json', 'r') as file:
	data = json.load(file)

gtype=data['operationalLayers'][0]['featureCollection']['layers'][0]['layerDefinition']['geometryType']
coordsys=data['operationalLayers'][0]['featureCollection']['layers'][0]['layerDefinition']['spatialReference']['latestWkid']
fieldsDat=data['operationalLayers'][0]['featureCollection']['layers'][0]['layerDefinition']['fields']
fieldNames=[n['name'] for n in fieldsDat]

datag={n:[]for n in fieldNames}
geoms=[]
for feature in data['operationalLayers'][0]['featureCollection']['layers'][0]['featureSet']['features']:
	geoms.append(MultiLineString(feature['geometry']['paths']))
	for key in datag:
		datag[key].append(feature['attributes'][key])

gdf=gpd.GeoDataFrame(data=datag,geometry=geoms,crs=('EPSG',str(coordsys)))
gdf.plot()
gdf.to_file(opj('shp',outFileName+'.shp'))
