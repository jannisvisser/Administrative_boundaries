import os
import sys
import numpy as np
import pandas as pd
from hdx.configuration import Configuration
from hdx.data.dataset import Dataset
import json


Configuration.create(hdx_site='prod', hdx_read_only=True)
tag='administrative boundaries'
datatypes=['zipped shapefile'] #,'ZIP']
downloadpath='C:/Users/JannisV/Rode Kruis/CP data/FME/Admin_data/zipfiles/api/'
df = pd.DataFrame()

def find_admin_level(name):
	#print(name)
	admin_level=99
	char=99
	pos=99
	for i in range(0,len(name)):
		if i==0:
			if name[i].isdigit() and not name[i+1].isdigit():
				char,pos=name[i],i
		elif i==len(name)-1:
			if name[i].isdigit() and not name[i-1].isdigit():
				char,pos=name[i],i
		else:
			if name[i].isdigit() and not name[i-1].isdigit() and not name[i+1].isdigit():
				char,pos=name[i],i
		if admin_level==99:
			admin_level=char
			prev_pos=pos
		elif 'adm' in name:
			if prev_pos < name.index('adm') < pos:
				admin_level=char
		if admin_level==99 and 'int' in name.lower():
			admin_level=0
	#print(admin_level)
	return admin_level

def get_field_names(shape_info,admin_level):
	d = json.loads(shape_info)
	pcode_col=''
	name_col=''
	pop_col=''
	field_names=''
	print(d)
	for attribute, value in d.items():
		#print(attribute)
		if attribute == 'layer_fields':
			field_names = value
			for i in range(0,len(field_names)):
				field_name = field_names[i]['field_name']
				if 'adm' in field_name:
					#print(field_name)
					field_admin_level = ''.join(c for c in field_name if c.isdigit())
					if field_admin_level == admin_level and 'code' in field_name:
						pcode_col = field_name
						print(pcode_col)
					elif field_admin_level == admin_level and 'name' in field_name:
						name_col = field_name
						print(name_col)
				elif 'pop' in field_name:
					pop_col = field_name
					print(pop_col)
	return pcode_col,name_col,pop_col,field_names
	

datasets = Dataset.search_in_hdx('',fq='tags:admin*')
dataset_id=1
for dataset in datasets:
	if tag in dataset.get_tags():
		location = dataset['solr_additions']
		country = location[(location.index('[')+2):(location.index(']')-1)]
		country = country.replace('\\\\u00f4','o')
		#print(country)
		if not ',' in country:
			country_dir = downloadpath + country + '/'
			if not os.path.exists(country_dir):
				os.makedirs(country_dir)
			resources = dataset.get_resources()
			resource_id=1
			for resource in resources:
				if resource['format'] in datatypes:
					#url, path = resource.download(country_dir)
					admin_level = find_admin_level(resource['name'])
					print(country)
					print(admin_level)
					pcode_col,name_col,pop_col,field_names=get_field_names(resource['shape_info'],admin_level)
					data = pd.DataFrame.from_records([{'dataset_id': dataset_id, 'resource_id': resource_id, 'country': country, 'name': resource['name'], 'adm': admin_level, 'link': resource['url'],'field_names': field_names,'pcode_col': pcode_col,'name_col': name_col,'pop_col': pop_col}])
					df = df.append(data)
					resource_id+=1
			dataset_id+=1

df.to_csv(downloadpath+'metadata_hdx_api.csv')	


