import os
import sys
import psycopg2
import osgeo.ogr
import shapely
import shapely.wkt
import pandas as pd
import geopandas as gpd
#%matplotlib inline


#Read metadata-table
pathname = os.path.dirname(os.path.abspath(__file__))
filename = 'metadata_admin_boundaries.csv'
path = pathname+'/'+filename
delim = ';'
df = pd.read_csv(path,delimiter=delim, encoding="windows-1251")

connection = psycopg2.connect(database="profiles",user="profiles", password="R3dCross+83")
cursor = connection.cursor()

for index,row in df.iterrows():
	
	#read variables from metadata
	country = row['country_code']
	admin_level = row['admin_level']
	pcode = row['pcode_col']
	name = row['name_col']
	pcode_parent = row['pcode_parent_col']
	population = row['population_col']
	filter = row['filter']
	
	if filter == 1:
	
		sql1 = 'CREATE SCHEMA IF NOT EXISTS "' + country.upper() + '_datamodel" ; DROP TABLE IF EXISTS "' + country.upper() + '_datamodel"."Geo_level' + str(admin_level) + '";'
		sql2a = 'SELECT ' + pcode + ' as pcode_level' + str(admin_level) + ', ' + name + ' as name'
		if isinstance(pcode_parent,str):
			sql2b = ', ' + pcode_parent + ' as pcode_level' + str(admin_level-1)
		else:
			sql2b = ''
		sql2c = ', geom INTO "' + country.upper() + '_datamodel"."Geo_level' + str(admin_level) + '" FROM geo_source.' + country + '_adm' + str(admin_level) + '_mapshaper;'
		sql2 = sql2a + sql2b + sql2c
		print(sql1)
		print(sql2)

		cursor.execute(sql1)
		cursor.execute(sql2)
		
		if isinstance(population,str):
			sql3 = 'DROP TABLE IF EXISTS "' + country.upper() + '_datamodel"."Indicators_' + str(admin_level) + '_population";'
			sql4 = 'SELECT ' + pcode + ' as pcode_level' + str(admin_level) + ', ' + population + ' as population into "' + country.upper() + '_datamodel"."Indicators_' + str(admin_level) + '_population" FROM geo_source.' + country + '_adm' + str(admin_level) + '_mapshaper;'
			sql5 = 'DROP TABLE IF EXISTS "' + country.upper() + '_datamodel"."Indicators_' + str(admin_level) + '_area";'
			sql6 = 'SELECT ' + pcode + ' as pcode_level' + str(admin_level) + ', st_area(st_transform(geom,4326)::geography)/1000000 as land_area into "' + country.upper() + '_datamodel"."Indicators_' + str(admin_level) + '_area" FROM geo_source.' + country + '_adm' + str(admin_level) + '_mapshaper;'
			print(sql3)
			print(sql4)
			print(sql5)
			print(sql6)
			
			cursor.execute(sql3)
			cursor.execute(sql4)
			cursor.execute(sql5)
			cursor.execute(sql6)
		
		connection.commit()