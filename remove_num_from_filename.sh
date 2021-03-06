#!/bin/bash

fudepoly_path="fudepolygon_data/*"
dirs=`find $fudepoly_path -name *.shp -o -name *.dbf -o -name *.prj -o -name *.shx`

for path in $dirs;
do
	filename=`basename $path`
	dirname=`dirname $path`
	nonum=$(echo $filename | tr -d [0-9])
	newpath="${dirname}/${nonum}"
	mv $path "$newpath"
	echo $newpath
done

echo
echo "finish renaming all files"
