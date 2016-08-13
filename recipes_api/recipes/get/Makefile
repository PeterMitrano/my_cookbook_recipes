all: zip upload

zip:
	mkdir -p build
	cp ./lambda_function.py build
	find -name "*.swp" | xargs rm -f
	cd build && zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbookRecipes --zip-file fileb://build/skill.zip
