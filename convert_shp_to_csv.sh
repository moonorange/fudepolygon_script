fudepoly_path="fudepolygon_data/*"
dirs=`find $fudepoly_path -name *.shp`

i=0
for path in $dirs;
do
	nonum=`echo $path | tr -d [0-9]`
	`mv $path $nonum`
	filename=`basename $path .shp`
	echo $filename
	# ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry, 4326) AS geom, * from $filename" $path.csv $path
	# let i++
done
