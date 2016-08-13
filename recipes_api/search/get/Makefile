all: zip upload

zip:
	mkdir -p build
	cp -r ../../../venv/lib/python2.7/site-packages/Levenshtein build
	cp -r ../../../venv/lib/python2.7/site-packages/fuzzywuzzy build
	cp ./lambda_function.py build
	find -name "*.swp" | xargs rm -f
	cd build && zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbookSearch --zip-file fileb://build/skill.zip
