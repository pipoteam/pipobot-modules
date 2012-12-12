#!/bin/bash

set -e

if [ -z "$1" ]; then
	echo "Usage: $0 <destination dir>"
	exit 1
fi

MYDIR=$(dirname $0)
DESTDIR=$1

mkdir -p $DESTDIR

for item in $MYDIR/*; do
	if [ -d "$item" -a "${item##*/}" != "distrib" -a -f "$item/__init__.py" ]; then
		cp -r $item $DESTDIR
	fi
done

touch "$DESTDIR/__init__.py"

find "$DESTDIR" -type d -exec chmod 755 {} \;
find "$DESTDIR" -type f -exec chmod 644 {} \;

chown -R root:root "$DESTDIR"

