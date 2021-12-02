#!/bin/bash

# Embeddia Project - Named Entity Recognition
# Copyright © 2020-2021 Luis Adrián Cabrera Diego - La Rochelle Université
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


LANGUAGE=$1
SHA_EMBEDDINGS=$2
echo $3

DIR=`dirname $0`

DIR=$DIR/fastText157

if [[ ! -d "$DIR" ]]
then
	echo "Creating directory"
    mkdir $DIR
    if [ $? -ne 0 ]; then { echo "Failed, aborting." ; exit 1; } fi
fi

#Set exit on error
set -e
catchKill () {
	echo "Process killed while: $2"
	removeFiles $3
}

catchExit () {
	# An error greater than 128 means a kill signal
	if [[ "$1" -lt "128" &&  "$1" -ne "0" ]]
	then
		echo "Error while: $2"
		removeFiles $3
	fi
	echo $1
}

removeFiles() {
	echo "Cleaning $DIR and removing $1"
		if [[ -d "$1" ]]
		then
			rm -r $1
		else
			if [[ -f "$1" ]]
			then
				rm $1
			fi
		fi
}

FILE="$DIR/cc.$LANGUAGE.300.vec.gz.top1.bin"
DOWNLOAD=1
if [ -f $FILE ]
then
	SHA_COMPARE=$(sha512sum $FILE | cut -d ' ' -f1)
	if [ "$SHA_EMBEDDINGS" == "$SHA_COMPARE" ]
	then
		MESSAGE="Embeddings already downloaded"
		echo $MESSAGE
		DOWNLOAD=0
	fi
fi

if [ "$DOWNLOAD" -eq "1" ]
then
	trap 'catchKill $? "$MESSAGE" "$FILE"' SIGINT
	trap 'catchExit $? "$MESSAGE" "$FILE"' EXIT

	FILE="$DIR/cc.$LANGUAGE.300.bin.gz"
	MESSAGE="Downloading embeddings"
	echo $MESSAGE
	wget -N -c https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.$LANGUAGE.300.bin.gz --directory-prefix=$DIR

	FILE="$DIR/cc.$LANGUAGE.300.vec.gz.top1.bin"
	MESSAGE="Unzipping embeddings"
	echo $MESSAGE
	gzip -dc <$DIR/cc.$LANGUAGE.300.bin.gz > $DIR/cc.$LANGUAGE.300.vec.gz.top1.bin

	FILE="$DIR/cc.$LANGUAGE.300.bin.gz"
	MESSAGE="Cleaning $DIR"
	echo $MESSAGE
	rm $DIR/cc.$LANGUAGE.300.bin.gz
fi
