#!/bin/bash
# Generate static html web site from iPython Notebooks.
# Source directory is <git>/<project>/src/notebook/*.ipynb
# Destination directory is <git>/<project>/site
# Existing site is demolished.
# HTML files are renamed to the iPython Notebook file extension.
# Otherwise hyperlinks to Notebooks are broken. 
cd `dirname $0`/../site
rm -f *.ipynb
cd ../src/notebook
export NETWORK_PROFILE=all_xr_versions
ipython3 nbconvert *.ipynb --profile=learning_lab --to=html --template=full --ExecutePreprocessor.enabled=True --ClearOutputPreprocessor.enabled=True
#ipython3 nbconvert *.ipynb --quiet --profile=learning_lab --to=html --template=full --ExecutePreprocessor.enabled=True --ClearOutputPreprocessor.enabled=True
#ipython3 nbconvert --quiet --profile=learning_lab --to=html --template=full --ClearOutputPreprocessor.enabled=True ../src/notebook/*.ipynb
#ipython3 nbconvert ../src/notebook/Settings.ipynb --profile=learning_lab --to=html --template=full --ExecutePreprocessor.enabled=True
mv *.html ../../site
cd ../../site
rename 's/\.html$/\.ipynb/' *.html
ls -1 *