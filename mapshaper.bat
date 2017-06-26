set input_folder="C:\Users\JannisV\Rode Kruis\CP data\FME\Admin_data\shapefiles"
cd %input_folder%
for /D %%a in (*) do (
	ECHO %%a
	cd %%a
	for %%x in (*.shp) do (
		ECHO %%x
		if not exist mapshaper mkdir mapshaper
		mapshaper "%%x" -simplify 10%% -o "mapshaper/%%a.shp"
	)
	cd ..
)
cd ..

