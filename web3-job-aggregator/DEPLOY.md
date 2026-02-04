# 🚀 Déploiement sur Render (Gratuit)

## Étape 1 : Push sur GitHub

```bash
cd ~/Desktop/web3-job-aggregator
git add .
git commit -m "Add web interface with Flask"
git push origin main
```

## Étape 2 : Créer un compte Render

1. Va sur https://render.com
2. Clique sur "Get Started"
3. Inscris-toi avec ton compte GitHub (recommandé)

## Étape 3 : Déployer l'app

1. **Dashboard Render** → Clique sur "New +"
2. Sélectionne **"Web Service"**
3. Connecte ton repo GitHub `web3-job-aggregator`
4. Configure :
   - **Name:** `web3-job-aggregator` (ou ce que tu veux)
   - **Region:** Frankfurt (le plus proche)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** **Free** 🆓
5. Clique sur **"Create Web Service"**

## Étape 4 : Attendre le déploiement

- ⏳ Ça prend 2-5 minutes
- Tu verras les logs de build
- Une fois terminé, tu auras une URL type : `https://web3-job-aggregator.onrender.com`

## ✅ C'est fait !

Ton site est en ligne ! 🎉

**URL exemple :** `https://ton-app.onrender.com`

## 🔧 Mises à jour automatiques

Chaque fois que tu push sur GitHub, Render redéploie automatiquement ! 🚀

```bash
# Faire une modification
git add .
git commit -m "Update something"
git push

# Render va automatiquement redéployer
```

## ⚠️ Note importante

Le tier gratuit de Render :
- ✅ Gratuit à vie
- ✅ Suffisant pour ton usage
- ⚠️ Se met en veille après 15min d'inactivité
- ⏳ Redémarre en ~30 secondes au premier accès

## 🎨 Personnaliser l'URL (Optionnel)

### Option 1 : Domaine Render gratuit
Dans les settings Render, change le nom : `mon-super-nom.onrender.com`

### Option 2 : Ton propre domaine (~10€/an)
1. Achète un domaine sur Namecheap/OVH
2. Dans Render Settings → Custom Domain
3. Ajoute ton domaine
4. Configure les DNS comme indiqué

## 🐛 Debug

Si ça marche pas :
1. Vérifie les logs dans Render Dashboard
2. Assure-toi que tous les fichiers sont pushés sur GitHub
3. Vérifie que `requirements.txt` est correct

## 🔥 Alternative rapide : Railway

Si Render ne marche pas, essaie Railway :

1. Va sur https://railway.app
2. "Start New Project" → "Deploy from GitHub"
3. Sélectionne ton repo
4. Railway détecte automatiquement Flask
5. Déploie !

C'est encore plus simple mais tu as que 5$ gratuit/mois.

## 💡 Test local avant de déployer

```bash
cd web3-job-aggregator
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Ouvre http://localhost:5000 dans ton navigateur
```

---

**Besoin d'aide ?** Ouvre une issue sur GitHub !
