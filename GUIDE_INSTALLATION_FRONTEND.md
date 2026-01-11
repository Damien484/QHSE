# 🚀 Guide d'installation Frontend - Interface Web QHSE

Ce guide vous aide à installer et lancer l'interface web moderne de l'application QHSE.

## ✅ Ce que vous avez déjà

Le **backend Flask** fonctionne parfaitement et est accessible sur http://localhost:5000

## 🎯 Ce que nous allons installer

Une **interface web professionnelle** avec React qui vous permettra de :
- 📊 Visualiser vos DUERP dans un dashboard moderne
- ➕ Créer des DUERP via un formulaire intuitif
- 👁️ Consulter les détails et statistiques
- 📥 Télécharger des PDF en un clic
- ✨ Profiter d'animations fluides et d'un design moderne

## 📋 Étape 1 : Installer Node.js (si pas déjà fait)

### Windows

1. Téléchargez Node.js depuis : **https://nodejs.org/**
2. Choisissez la version **LTS** (Long Term Support)
3. Lancez l'installateur `.msi` et suivez les instructions
4. Acceptez tous les paramètres par défaut

### Vérification

Ouvrez PowerShell et tapez :

```powershell
node --version
npm --version
```

Vous devriez voir quelque chose comme :
```
v18.17.0
9.6.7
```

✅ Si vous voyez des numéros de version, c'est bon !

## 📦 Étape 2 : Installer les dépendances React

### Sur Windows (PowerShell)

```powershell
# Naviguer vers le dossier frontend
cd C:\Users\qhse-\Documents\QHSE\frontend

# Installer toutes les dépendances
npm install
```

⏱️ **Temps d'installation** : 2-5 minutes (cela télécharge ~200 MB de bibliothèques)

Vous verrez plein de texte défiler, c'est normal ! npm est en train de télécharger et installer toutes les bibliothèques React nécessaires.

### Résultat attendu

À la fin, vous devriez voir :

```
added 1456 packages, and audited 1457 packages in 2m

153 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

✅ Parfait ! Les dépendances sont installées.

## 🚀 Étape 3 : Lancer l'application web

### Assurez-vous que le backend tourne

**Terminal 1** (gardez-le ouvert) :
```powershell
cd C:\Users\qhse-\Documents\QHSE
.\venv\Scripts\Activate.ps1
python run.py
```

Vous devriez voir :
```
🚀 Démarrage de l'application QHSE en mode development
📍 L'API est accessible sur http://localhost:5000
```

### Lancez le frontend

**Terminal 2** (nouveau PowerShell) :
```powershell
cd C:\Users\qhse-\Documents\QHSE\frontend
npm start
```

⏱️ **Première fois** : 20-30 secondes de compilation

Vous verrez :
```
Compiled successfully!

You can now view qhse-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.17:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

## 🎉 L'application va s'ouvrir automatiquement !

Votre navigateur va s'ouvrir sur **http://localhost:3000** et vous verrez :

- ✨ Un magnifique dashboard avec animations
- 📊 Des cartes de statistiques
- 🎨 Un design professionnel bleu/blanc
- 📱 Une navigation sur la gauche

## 🎨 Navigation dans l'interface

### Menu latéral

- **📊 Tableau de bord** - Statistiques et vue d'ensemble
- **📄 Mes DUERP** - Liste de tous vos DUERP
- **➕ Nouveau DUERP** - Créer un nouveau document

### Fonctionnalités disponibles

1. **Tableau de bord** (`/`)
   - Vue d'ensemble avec statistiques
   - Cartes animées
   - Informations sur l'utilisation

2. **Liste des DUERP** (`/duerp`)
   - Affichage en cartes
   - Statut de chaque DUERP
   - Bouton pour voir les détails

3. **Créer un DUERP** (`/duerp/nouveau`)
   - Formulaire step-by-step en 3 étapes
   - Validation des champs
   - Redirection automatique après création

4. **Détails d'un DUERP** (`/duerp/:id`)
   - Informations complètes
   - Statistiques détaillées
   - Téléchargement PDF en un clic
   - Liste des unités de travail

## 🧪 Test rapide

### 1. Créer un premier DUERP

1. Cliquez sur **"Nouveau DUERP"** dans le menu
2. Remplissez le formulaire :
   - Nom entreprise : "Ma Société Test"
   - SIRET : "12345678901234"
   - Effectif : 25
   - Cliquez **"Suivant"**
3. Renseignez le responsable (optionnel)
4. Cliquez **"Créer le DUERP"**

✅ Vous serez redirigé vers la page de détails du DUERP créé !

### 2. Voir la liste

1. Cliquez sur **"Mes DUERP"** dans le menu
2. Vous verrez une carte avec votre DUERP
3. Cliquez sur **"Voir les détails"**

### 3. Télécharger le PDF

1. Sur la page de détails d'un DUERP
2. Cliquez sur **"Télécharger PDF"**
3. Le document se télécharge automatiquement !

## 🔄 Utilisation quotidienne

### Pour lancer l'application

**Chaque fois** que vous voulez utiliser l'application :

1. **Terminal 1** - Backend :
   ```powershell
   cd C:\Users\qhse-\Documents\QHSE
   .\venv\Scripts\Activate.ps1
   python run.py
   ```

2. **Terminal 2** - Frontend :
   ```powershell
   cd C:\Users\qhse-\Documents\QHSE\frontend
   npm start
   ```

3. Ouvrez votre navigateur sur **http://localhost:3000**

### Pour arrêter l'application

- Dans chaque terminal, appuyez sur **Ctrl+C**

## 🎨 Personnalisation

### Changer les couleurs

Éditez le fichier `frontend/src/theme.js` :

```javascript
primary: {
  main: '#1976d2', // Changez cette couleur
}
```

### Modifier le titre

Éditez `frontend/public/index.html` :

```html
<title>QHSE - Votre Entreprise</title>
```

## 🐛 Dépannage

### Erreur "npm n'est pas reconnu"

Node.js n'est pas installé correctement. Réinstallez depuis nodejs.org.

### Erreur lors de npm install

```powershell
# Nettoyer et réinstaller
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### L'application ne se lance pas

1. Vérifiez que le backend tourne
2. Vérifiez qu'aucune erreur ne s'affiche dans le terminal
3. Essayez de redémarrer (Ctrl+C puis npm start)

### Erreur "Port 3000 already in use"

Un autre processus utilise le port 3000 :

```powershell
# Utiliser un autre port
$env:PORT=3001
npm start
```

### Les modifications ne s'affichent pas

Le hot reload fonctionne automatiquement, mais si ça ne marche pas :
1. Ctrl+C pour arrêter
2. Relancer `npm start`

### Erreurs de connexion API

1. Vérifiez que le backend tourne sur http://localhost:5000
2. Testez l'API dans le navigateur : http://localhost:5000/health
3. Regardez la console du navigateur (F12) pour voir les erreurs

## 📱 Version mobile

L'interface est **entièrement responsive** ! Vous pouvez :
- Accéder depuis votre téléphone sur le même réseau
- Utiliser l'adresse affichée : `http://192.168.1.17:3000`

## 🎯 Prochaines étapes

Maintenant que vous avez l'interface, vous pouvez :

1. ✅ Créer vos DUERP via l'interface
2. ✅ Visualiser les statistiques
3. ✅ Télécharger des PDF

## 💡 Astuces

- **F12** dans le navigateur pour ouvrir les DevTools
- **Ctrl+R** pour recharger la page
- **Ctrl+Shift+I** pour inspecter un élément

## 📚 En savoir plus

- Voir `frontend/README.md` pour plus de détails techniques
- Documentation React : https://react.dev/
- Documentation Material-UI : https://mui.com/

## ✅ Checklist finale

- [ ] Node.js installé (node --version fonctionne)
- [ ] npm install terminé sans erreur
- [ ] Backend lancé (http://localhost:5000 fonctionne)
- [ ] Frontend lancé (http://localhost:3000 s'ouvre)
- [ ] Vous voyez le dashboard avec animations
- [ ] Vous pouvez créer un DUERP
- [ ] Vous pouvez télécharger un PDF

🎉 **Félicitations ! Vous avez maintenant une application QHSE complète avec une interface moderne !**
