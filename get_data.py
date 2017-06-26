import os
import sys
import pandas as pd
from urllib.request import urlopen
import zipfile
import psycopg2
import shapefile
import glob
import io
import math

#Read metadata-table
pathname = os.path.dirname(os.path.abspath(__file__))
filename = 'metadata_admin_boundaries.csv'
path = pathname+'/'+filename
delim = ';'
df = pd.read_csv(path,delimiter=delim, encoding="windows-1251")
#Create zipfiles-folder
zip_dir = 'zipfiles/'
if not os.path.exists(zip_dir):
	os.makedirs(zip_dir)

#Loop through metadata to download and unzip all admin-files
for index,row in df.iterrows():
	
	#read variables from metadata
	country = row['country_code']
	admin_level = row['admin_level']
	zipURL = row['link'] #'https://data.humdata.org/dataset/5ed05f6e-556f-4545-918a-a5b679386ee9/resource/bcc9d500-3895-4262-8e6f-9eb3b652d931/download/lka_pop_censusproj2022adm2_wfpocha.zip'
	filter = row['filter']
	print(filter)
	
	if filter == 1:
		#create additional variables
		item = country + '_adm' + str(admin_level)
		print(item)
		dirname = 'shapefiles/' + item + '/'
		filename = item + '.zip'
		
		#Create extraction-directory
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		
		#Download zipfile
		zip = urlopen(zipURL).read()
		with open(zip_dir+filename,'wb') as f:
			f.write(zip)
			
		#Unzip
		zfobj = zipfile.ZipFile(zip_dir+filename)
		print(zfobj.namelist())
		for name in zfobj.namelist():
			if not name.endswith('/'):
				if '/' in name:
					filename = name.split('/')[1]
				else:
					filename = name
				print(filename)
				uncompressed = zfobj.read(name)	
				outputFilename = dirname + filename
				output = open(outputFilename,'wb')
				output.write(uncompressed)
				output.close()	
	



		


