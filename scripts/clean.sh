echo Removing venv folder...
rm -r venv
echo

echo removing models folder
rm -r ./src/nlp/models

echo removing __pycache__ folders
find . -name __pycache__ -exec rm -rf {} \;

echo removing logs folder
rm -r log

echo Cleaning Complete.