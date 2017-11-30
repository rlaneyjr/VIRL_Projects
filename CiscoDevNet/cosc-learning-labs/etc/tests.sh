#!/bin/bash

BAD=0
#Run tests
for f in ../test/*.py; do
	if ! python ${f}; then BAD=1; fi
done

#Run static analysis
./process_pylint.sh || BAD=1

#Process Markdown files
source ./process_mdmerge.sh || BAD=1

exit $BAD
