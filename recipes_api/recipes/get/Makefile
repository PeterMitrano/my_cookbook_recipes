all: zip upload

zip:
	zip -q -r skill.zip *.py

upload: zip
	aws lambda update-function-code --function-name MyCookbookRecipes --zip-file fileb://skill.zip
