# because Jose cannot seem to remember the exact steps each time...
if [[ ! $(sudo echo 0) ]]; then exit; fi
rm -rf dist build specimen_tools.egg-info
python setup.py bdist_wheel
twine upload dist/*
