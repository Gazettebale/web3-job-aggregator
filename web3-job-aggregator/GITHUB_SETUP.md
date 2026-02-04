# 🚀 Guide : Publier sur GitHub

## Étape 1 : Créer le repo sur GitHub.com

1. Va sur https://github.com
2. Clique sur le **+** en haut à droite → **New repository**
3. Remplis les infos :
   - **Repository name:** `web3-job-aggregator`
   - **Description:** `🔍 Aggregate Web3/crypto job listings from 13+ job boards in one place`
   - **Public** (pour que ce soit visible dans ton portfolio)
   - ✅ Coche **Add a README file** (on l'écrasera avec le nôtre)
   - **Add .gitignore:** Python
   - **Choose a license:** MIT License
4. Clique sur **Create repository**

## Étape 2 : Sur ton Mac (à midi)

### A. Clone le repo que tu viens de créer

```bash
cd ~/Documents  # ou là où tu veux mettre le projet
git clone https://github.com/TON-USERNAME/web3-job-aggregator.git
cd web3-job-aggregator
```

### B. Copie tous les fichiers du ZIP

```bash
# Décompresse le ZIP que tu as téléchargé
unzip ~/Downloads/web3-job-aggregator.zip

# Copie tous les fichiers dans le repo
cp -r web3-job-aggregator/* .

# Ou manuellement :
# - Ouvre le ZIP
# - Copie tous les fichiers dans le dossier web3-job-aggregator
```

### C. Push sur GitHub

```bash
# Ajoute tous les fichiers
git add .

# Commit
git commit -m "Initial commit: Web3 job aggregator with 13 job boards"

# Push
git push origin main
```

## Étape 3 : Personnalise le README

Avant de push, édite le `README.md` et remplace `TON-USERNAME` par ton vrai username GitHub :

```bash
# Trouve et remplace
sed -i '' 's/TON-USERNAME/ton-vrai-username/g' README.md
sed -i '' 's/TON-USERNAME/ton-vrai-username/g' QUICKSTART.md

# Ou édite manuellement avec VS Code / nano / vim
```

## Étape 4 : Test avant de publier (optionnel)

```bash
# Installe les dépendances
pip3 install -r requirements.txt

# Teste que ça marche
python3 test_aggregator.py

# Si OK, push !
git push origin main
```

## 🎨 Bonus : Rendre le repo plus attractif

### Ajouter des badges au README

Ajoute en haut du README.md :

```markdown
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
```

### Créer un GitHub Action pour tester automatiquement

Crée `.github/workflows/test.yml` :

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run test
      run: python test_aggregator.py
```

### Ajouter des topics sur GitHub

Sur la page du repo :
- Clique sur l'engrenage à côté de "About"
- Ajoute ces topics : `web3`, `crypto`, `job-board`, `scraping`, `python`, `automation`, `blockchain`

## 🔥 Structure finale du repo

```
web3-job-aggregator/
├── .github/
│   └── workflows/
│       └── test.yml
├── .gitignore
├── LICENSE
├── README.md
├── QUICKSTART.md
├── EXAMPLE_OUTPUT.md
├── requirements.txt
├── config.py
├── web3_job_aggregator.py
├── auto_search.py
└── test_aggregator.py
```

## 📱 Commandes rapides

```bash
# Setup complet en une fois
git clone https://github.com/TON-USERNAME/web3-job-aggregator.git
cd web3-job-aggregator
# Copie les fichiers du ZIP ici
git add .
git commit -m "Initial commit: Web3 job aggregator"
git push origin main

# Utilisation
pip3 install -r requirements.txt
python3 web3_job_aggregator.py
```

## ✅ Checklist

- [ ] Repo créé sur GitHub.com
- [ ] Repo cloné sur Mac
- [ ] Fichiers du ZIP copiés
- [ ] Username personnalisé dans README
- [ ] Testé localement
- [ ] Push sur GitHub
- [ ] Topics ajoutés
- [ ] Description mise à jour

Voilà ! Ton repo sera nickel pour ton portfolio ! 🎯
