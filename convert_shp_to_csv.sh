#!/bin/bash

fudepoly_path="fudepolygon_data/*"
dirs=`find $fudepoly_path -name *.shp`
total_num=`find . -name *.shp | wc -l`

i=0
for path in $dirs;
do
	filename=`basename $path .shp`
	ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry, 4326) AS geom, * from $filename" "csv/$filename.csv" $path
	let i++
	echo "$filename $i"
done

echo
echo "finish converting $i files"
