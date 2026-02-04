# 🤝 Contributing to Web3 Job Aggregator

Merci de ton intérêt pour contribuer ! 🎉

## Comment contribuer

### 🐛 Reporter un bug

1. Vérifie que le bug n'a pas déjà été reporté dans les [Issues](https://github.com/TON-USERNAME/web3-job-aggregator/issues)
2. Ouvre une nouvelle issue avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Version de Python utilisée
   - Message d'erreur complet

### ✨ Proposer une nouvelle fonctionnalité

1. Ouvre une issue pour discuter de l'idée
2. Attends le feedback avant de commencer à coder
3. Fork le repo et crée une branche
4. Développe la feature
5. Soumets une Pull Request

### 📋 Ajouter un nouveau job board

C'est super simple ! Voici comment faire :

1. **Fork le repo**

2. **Édite `web3_job_aggregator.py`**

Ajoute ton job board dans `self.job_boards` :

```python
'nouveau_site': {
    'name': 'Nom du Site',
    'url': 'https://example.com/jobs',
    'enabled': True
}
```

3. **Teste localement**

```bash
python3 web3_job_aggregator.py
```

4. **Commit et Push**

```bash
git add web3_job_aggregator.py
git commit -m "Add [Nom du Site] job board"
git push origin main
```

5. **Crée une Pull Request**

Dans la description, mentionne :
- Nom du job board
- URL
- Pourquoi c'est utile
- Screenshot du résultat (optionnel)

### 🔧 Améliorer le scraping

Si un site ne fonctionne pas bien :

1. Identifie le problème (sélecteurs HTML, structure, etc.)
2. Crée une fonction de scraping spécifique si nécessaire
3. Teste avec plusieurs pages du site
4. Soumets une PR avec des exemples

### 📝 Améliorer la documentation

- README.md : documentation principale
- QUICKSTART.md : guide rapide
- Code comments : explications dans le code
- Examples : ajoute des cas d'usage

### ✅ Checklist avant de soumettre une PR

- [ ] Le code fonctionne localement
- [ ] Pas d'erreurs Python
- [ ] La documentation est mise à jour si nécessaire
- [ ] Les commentaires sont clairs
- [ ] Le commit message est descriptif

## 💡 Idées de contributions

### Facile
- Ajouter de nouveaux job boards
- Corriger des typos
- Améliorer les messages d'erreur
- Ajouter des exemples

### Moyen
- Améliorer les sélecteurs HTML pour certains sites
- Ajouter des filtres (salaire, expérience, etc.)
- Créer une interface en ligne de commande plus riche
- Ajouter des tests unitaires

### Avancé
- API REST avec FastAPI
- Interface web avec Flask/React
- Base de données pour historique
- Notifications (email, Telegram, Discord)
- Support d'APIs officielles quand disponibles
- Machine learning pour recommandations

## 🎨 Style de code

- Utilise des noms de variables descriptifs
- Ajoute des docstrings aux fonctions
- Suis PEP 8 (utilise `black` pour formatter)
- Commente le code complexe

## 📞 Questions ?

- Ouvre une [Discussion](https://github.com/TON-USERNAME/web3-job-aggregator/discussions)
- Ou crée une [Issue](https://github.com/TON-USERNAME/web3-job-aggregator/issues)

Merci pour ta contribution ! 🚀
