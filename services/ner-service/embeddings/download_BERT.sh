#!/bin/bash

# Embeddia Project - Named Entity Recognition
# Copyright © 2021 Luis Adrián Cabrera Diego - La Rochelle Université
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


DIR=/ner_service/data/embeddings

DIR="$DIR/bert-base-multilingual-cased"

if [[ ! -d "$DIR" ]]
then
	echo "Creating directory"
    mkdir -p $DIR
    if [ $? -ne 0 ]; then { echo "Failed, aborting." ; exit 1; } fi
fi

DOWNLOAD=1

if [ -f "$DIR/vocab.txt" ] && [ -f "$DIR/config.json" ] && [ -f "$DIR/pytorch_model.bin" ]
then
	cd $DIR
	sha512sum -c ../bert_sha.txt --quiet --status --strict
	DOWNLOAD=$?
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

if [ "$DOWNLOAD" -ne "0" ]
then

	trap 'catchKill $? "$MESSAGE" "$FILE"' SIGINT
	trap 'catchExit $? "$MESSAGE" "$FILE"' EXIT
	
	FILE="$DIR/vocab.txt"
	MESSAGE="Downloading vocab"
	wget -c -N https://huggingface.co/bert-base-multilingual-cased/resolve/main/vocab.txt --directory-prefix=$DIR
	
	FILE="$DIR/config.json"
	MESSAGE="Downloading config"
	wget -c -N https://huggingface.co/bert-base-multilingual-cased/resolve/main/config.json --directory-prefix=$DIR
	
	FILE="$DIR/pytorch_model.bin"
	MESSAGE="Downloading bin"
	wget -c -N https://huggingface.co/bert-base-multilingual-cased/resolve/main/pytorch_model.bin --directory-prefix=$DIR
fi
