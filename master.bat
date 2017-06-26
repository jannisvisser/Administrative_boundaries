REM --> Get data through python-script, which downloads, saves and unzips all admin-files from a metadata-csv 
call python get_data.py

REM --> Load all shapefiles into PostGIS
set input_folder="C:\Users\JannisV\Rode Kruis\CP data\FME\Admin_data\shapefiles"
set PG_connection="PG:host=localhost user=profiles dbname=profiles password=R3dCross+83 active_schema=geo_source"

cd %input_folder%
for /D %%a in (*) do (
	ECHO %%a
	cd %%a
	for /r %%x in (*.shp) do (
		ogr2ogr -f 'PostgreSQL' %PG_connection% "%%x" -lco GEOMETRY_NAME=geom -lco FID=gid -lco PRECISION=no -nlt PROMOTE_TO_MULTI -nln "%%a" -overwrite
		ogr2ogr -f 'PostgreSQL' %PG_connection% "mapshaper/%%a.shp" -lco GEOMETRY_NAME=geom -lco FID=gid -lco PRECISION=no -nlt PROMOTE_TO_MULTI -nln "%%a_mapshaper" -overwrite
	)
	cd ..
)
cd ..