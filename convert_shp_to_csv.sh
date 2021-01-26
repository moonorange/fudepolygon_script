filename=`basename $path .shp`
ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry, 4326) AS geom, * from $filename" $path.csv $path
