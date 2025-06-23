#!/bin/bash

# используется для переименования папок типа чистый и размеченный к единому
# стандарту "чист" и "разм"

for dir in /home/tim/Desktop/dataset/*/*/
do
    #echo renames subdirs in folder ${dir}
    MARKEDDIR="$dir"разм/
    if [ -d "$MARKEDDIR" ]; then
        echo dir already exists "$dir"разм/ 
    else
        echo renamed dir "$dir"*азм*
        mv "$dir"*азм* "$dir"разм/
    fi

    CLEARDIR="$dir"чист/
    if [ -d "$CLEARDIR" ]; then
        echo dir already exists "$dir"чист/ 
    else
        echo renamed dir "$dir"*ист*
        mv "$dir"*ист* "$dir"чист/
    fi

done
