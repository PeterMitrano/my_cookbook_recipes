all: zip upload

zip:
	zip -q -r skill.zip *.py \
		../../../venv/lib/python2.7/site-packages/Levenshtein \
		../../../venv/lib/python2.7/site-packages/fuzzywuzzy

upload: zip
	aws lambda update-function-code --function-name MyCookbookSearch --zip-file fileb://skill.zip
