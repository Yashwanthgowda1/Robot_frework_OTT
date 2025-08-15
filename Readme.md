# Robot_frework_OTT


pip list > requirements.txt


<!-- install the dependences -->

pip install -r requirements.txt

pip install -r requirements.txt --upgrade

pip install -r requirements.txt --upgrade --force-reinstall


<!-- ingorning the file while pushing ex:results at evry time -->

echo results/ >> .gitignore

<!-- stop tracking -->
git rm -r --cached results

<!-- commit changes -->
git add .gitignore
git commit -m "Ignore results folder from tracking"


