1. Cloner le repo
```
git clone git@github.com:Orangetine/INPN-Images-Scrap.git INPN_images_scrap
```
2. Installer poetry
```
curl -sSL https://install.python-poetry.org | python3 -
```
3. Verifier l'install
```
poetry --version
```
4. Autoriser la création d'un environnement virtuel
```
poetry config virtualenvs.in-project true
```
5. Installer l'environnement virtuel
```
poetry install
```
6. Activer l'environnement virtuel
```
source .venv/bin/activate
```
7. Exécuter le script
``` 
python inpn_images.py
```