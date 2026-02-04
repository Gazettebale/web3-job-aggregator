# 🚀 Guide Rapide - Web3 Job Aggregator

## Installation en 2 minutes

```bash
# 1. Clone le repo
git clone https://github.com/TON-USERNAME/web3-job-aggregator.git
cd web3-job-aggregator

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Lance l'outil
python web3_job_aggregator.py
```

## Utilisation Basique

### Chercher tous les jobs
```bash
python web3_job_aggregator.py
# Appuie sur Enter quand demandé pour voir TOUS les jobs
```

### Chercher avec des mots-clés
```bash
python web3_job_aggregator.py
# Entre: solidity, remote, developer
```

### Exemples de recherches utiles

**Pour développeur Solidity :**
```
Keywords: solidity, smart contract, remote
```

**Pour développeur Rust :**
```
Keywords: rust, solana, avalanche, remote
```

**Pour rôle Product/Marketing :**
```
Keywords: product manager, marketing, community
```

**Pour développeur DeFi :**
```
Keywords: defi, protocol, developer, remote
```

## Où sont mes résultats ?

Après l'exécution, tu auras :
- `web3_jobs.json` - Toutes les offres en JSON
- `web3_jobs.md` - Version lisible en Markdown

## Personnalisation Rapide

### Éditer les job boards

Ouvre `web3_job_aggregator.py` et trouve `self.job_boards`:

```python
# Pour désactiver un site, change 'enabled' à False
'midnight': {
    'name': 'Midnight Network',
    'url': 'https://midnight.network/careers',
    'enabled': False  # ← Désactivé
}
```

### Ajouter ton propre site

```python
'mon_site': {
    'name': 'Mon Job Board',
    'url': 'https://example.com/jobs',
    'enabled': True
}
```

## Automatisation

### Lancer tous les jours automatiquement (Linux/Mac)

```bash
# Édite ton crontab
crontab -e

# Ajoute cette ligne pour lancer à 9h tous les jours
0 9 * * * cd /path/to/web3-job-aggregator && python3 web3_job_aggregator.py
```

### Script rapide pour chercher sans interaction

Crée `auto_search.py` :

```python
from web3_job_aggregator import Web3JobAggregator

aggregator = Web3JobAggregator()
jobs = aggregator.search_all(keywords=['solidity', 'remote'])
aggregator.save_json()
aggregator.save_markdown()
print(f"✅ {len(jobs)} jobs trouvés!")
```

Lance avec :
```bash
python auto_search.py
```

## Astuces

1. **Trop de résultats ?** → Utilise plus de mots-clés spécifiques
2. **Pas assez de résultats ?** → Utilise moins de mots-clés ou des termes plus généraux
3. **Site ne fonctionne pas ?** → Désactive-le temporairement dans le code
4. **Besoin d'aide ?** → Ouvre une issue sur GitHub

## Troubleshooting

### Erreur "No module named 'requests'"
```bash
pip install requests beautifulsoup4 lxml
```

### Erreur "Connection timeout"
- Vérifie ta connexion Internet
- Certains sites peuvent être lents, attends un peu plus

### Trop de duplicatas
- C'est normal ! Le script déduplique automatiquement
- Les sites partagent souvent les mêmes offres

## Prochaines étapes

1. ⭐ Star le repo si ça t'a aidé !
2. 🍴 Fork et personnalise pour tes besoins
3. 🤝 Contribue en ajoutant de nouveaux sites
4. 💼 Trouve ton job de rêve dans le Web3 !

**Happy hunting! 🎯**
