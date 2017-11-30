#!/bin/bash

#Setup the environment
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv python-apic-em-samples
workon python-apic-em-samples
pip install requests
pip install MarkdownTools2
pip install pylint

#Run tests
python ../test/tests.py

#Run static analysis
./process_pylint.sh

#Process Markdown files
source ./process_mdmerge.sh