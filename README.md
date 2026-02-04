# 🚀 Web3 Job Aggregator

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/TON-USERNAME/web3-job-aggregator/graphs/commit-activity)

Un outil Python pour agréger et rechercher des offres d'emploi Web3/Crypto à partir de **13 job boards** en un seul endroit.

## 📋 Fonctionnalités

- ✅ Scraping automatique de 13 job boards Web3
- 🔍 Recherche par mots-clés (remote, solidity, developer, etc.)
- 💾 Export en JSON et Markdown
- 🎯 Centralisation de toutes les offres au même endroit
- 🧹 Déduplication automatique des offres
- 📊 Groupement par source
- 🔄 Facilement extensible avec de nouveaux sites

## 🌐 Job Boards Intégrés (13)

1. **Crypto Careers** - https://www.crypto-careers.com/
2. **Web3 Career** - https://web3.career/
3. **Cryptocurrency Jobs** - https://cryptocurrencyjobs.co/
4. **Crypto Jobs List** - https://cryptojobslist.com/
5. **BeInCrypto Jobs** - https://beincrypto.com/jobs/
6. **JobStash** - https://jobstash.xyz/jobs
7. **Remote3** - https://www.remote3.co/
8. **Midnight Network** - https://midnight.network/careers
9. **Dragonfly** - https://jobs.dragonfly.xyz/jobs
10. **Block** - https://block.xyz/careers/jobs
11. **Solana Jobs** - https://jobs.solana.com/jobs
12. **Avalanche Jobs** - https://jobs.avax.network/jobs
13. **Ethereum Job Board** - https://www.ethereumjobboard.com/jobs

## 🛠️ Installation

### Prérequis
- Python 3.7+
- pip

### Étapes d'installation

1. Clone ce repository :
```bash
git clone https://github.com/Gazettebale/web3-job-aggregator.git
cd web3-job-aggregator
```

2. Installe les dépendances :
```bash
pip install -r requirements.txt
```

Ou avec pip3 :
```bash
pip3 install -r requirements.txt
```

## 🚀 Utilisation

### Mode Simple (Recommandé)

Lance le script et suis les instructions :
```bash
python web3_job_aggregator.py
```

Ou avec python3 :
```bash
python3 web3_job_aggregator.py
```

**Exemple d'utilisation :**
```
Keywords: solidity, remote, developer

⏳ Starting search...

⏳ Fetching from Crypto Careers... ✅ 12 jobs
⏳ Fetching from Web3 Career... ✅ 23 jobs
⏳ Fetching from Cryptocurrency Jobs... ✅ 18 jobs
...

✨ TOTAL: 156 unique jobs found
```

### Mode Programmatique

Utilise l'outil dans ton propre code Python :

```python
from web3_job_aggregator import Web3JobAggregator

# Créer une instance
aggregator = Web3JobAggregator()

# Rechercher des jobs avec filtres
keywords = ['solidity', 'smart contract', 'remote']
jobs = aggregator.search_all(keywords=keywords)

# Afficher les résultats
aggregator.display(limit=10)

# Sauvegarder
aggregator.save_json('mes_jobs.json')
aggregator.save_markdown('mes_jobs.md')

# Accéder aux jobs directement
for job in aggregator.jobs:
    print(f"{job['title']} at {job['company']}")
```

## 📊 Format de sortie

### JSON (`web3_jobs.json`)
```json
{
  "total_jobs": 156,
  "last_updated": "2026-02-04T10:30:00",
  "jobs": [
    {
      "title": "Senior Solidity Developer",
      "company": "Acme Protocol",
      "location": "Remote",
      "url": "https://web3.career/job/123",
      "source": "Web3 Career",
      "scraped_at": "2026-02-04T10:30:00"
    }
  ]
}
```

### Markdown (`web3_jobs.md`)
Format lisible groupé par source avec tous les détails des offres.

## 🔧 Personnalisation

### Méthode 1: Via config.py

Édite `config.py` pour personnaliser :

```python
# Mots-clés par défaut
DEFAULT_KEYWORDS = [
    'rust',
    'solana', 
    'defi',
    'smart contract'
]

# Désactiver certains job boards
JOB_BOARDS = {
    'crypto-careers': {
        'enabled': True  # Change à False pour désactiver
    },
    # ...
}
```

### Méthode 2: Ajouter un nouveau job board

Dans `web3_job_aggregator.py`, ajoute dans `self.job_boards` :

```python
'nouveau_site': {
    'name': 'Nouveau Site',
    'url': 'https://example.com/jobs',
    'enabled': True
}
```

### Exemples de mots-clés utiles

**Par rôle :**
- `developer`, `engineer`, `architect`
- `product manager`, `designer`, `marketing`
- `analyst`, `researcher`, `writer`

**Par techno :**
- `solidity`, `rust`, `move`, `cairo`
- `react`, `typescript`, `python`

**Par domaine :**
- `defi`, `nft`, `dao`, `gaming`
- `layer 2`, `zkp`, `mev`, `staking`

**Par type :**
- `remote`, `full-time`, `contract`
- `senior`, `junior`, `lead`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à :
- Ajouter de nouveaux job boards
- Améliorer le scraping
- Corriger des bugs
- Proposer de nouvelles fonctionnalités

## ⚠️ Notes importantes

1. **Rate Limiting** : Le script inclut des délais entre les requêtes (1 seconde) pour être respectueux des serveurs.

2. **Web Scraping Ethics** : Certains sites peuvent avoir des APIs officielles. Vérifie toujours les Terms of Service avant de scraper.

3. **Maintenance** : Les structures HTML des sites peuvent changer. Le script nécessitera peut-être des ajustements réguliers.

4. **APIs** : Pour une solution plus robuste, considère utiliser les APIs officielles quand elles sont disponibles :
   - Certains job boards offrent des APIs
   - Greenhouse API pour les entreprises qui l'utilisent
   - Lever API, etc.

## 🔮 Améliorations futures

- [ ] Support API pour les sites qui en ont une
- [ ] Base de données SQLite pour historique
- [ ] Interface web avec Flask/FastAPI
- [ ] Notifications email/Telegram pour nouvelles offres
- [ ] Filtres avancés (salaire, expérience, etc.)
- [ ] Déduplication automatique des offres
- [ ] Scraping planifié (cron job)

## 📝 License

MIT License - Fais-en ce que tu veux !

## 🙏 Remerciements

Merci aux job boards Web3 qui rendent l'information accessible !

---

**Happy job hunting! 🎯**

Pour des questions ou suggestions : ouvre une issue sur GitHub
