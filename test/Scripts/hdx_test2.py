import os
import sys
#import pandas as pd
from hdx.configuration import Configuration
from hdx.data.dataset import Dataset

old_stdout = sys.stdout
log_file = open("C:/Users/JannisV/Rode Kruis/CP data/FME/Admin_data/message_dataset.log","w")
sys.stdout = log_file

Configuration.create(hdx_site='prod', hdx_read_only=True)
tag='administrative boundaries'
datatype='zipped shapefile'
downloadpath='C:/Users/JannisV/Rode Kruis/CP data/FME/Admin_data/zipfiles/api/'

datasets = Dataset.search_in_hdx('',fq='tags:admin*',rows=10)
#print(datasets)
for dataset in datasets:
	if tag in dataset.get_tags():
		resources = dataset.get_resources()
		for resource in resources:
			if resource['format'] == datatype:
				print(resources)
				#folder = downloadpath+dataset['name']
				#if not os.path.exists(folder):
				#	os.makedirs(folder)
				#url, path = resource.download(folder)
			
sys.stdout = old_stdout

log_file.close()			
