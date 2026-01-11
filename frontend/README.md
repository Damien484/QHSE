# Frontend React - Application QHSE

Interface web moderne pour la gestion des DUERP (Documents Uniques d'Évaluation des Risques Professionnels).

## 🎨 Technologies utilisées

- **React 18** - Framework JavaScript
- **Material-UI (MUI)** - Bibliothèque de composants UI
- **React Router** - Navigation
- **Axios** - Client HTTP
- **Framer Motion** - Animations fluides

## 📋 Prérequis

- **Node.js 16+** et **npm** installés sur votre machine
- Backend Flask en cours d'exécution sur `http://localhost:5000`

## 🚀 Installation

### 1. Installer Node.js

Si vous n'avez pas Node.js, téléchargez-le depuis : https://nodejs.org/

**Vérifiez l'installation** :
```bash
node --version
npm --version
```

### 2. Installer les dépendances

Dans le dossier `frontend` :

```bash
cd frontend
npm install
```

Cette commande va installer toutes les dépendances listées dans `package.json`.

⏱️ **Temps d'installation** : 2-5 minutes selon votre connexion internet.

## 🎯 Lancer l'application

### Démarrage

```bash
npm start
```

L'application va s'ouvrir automatiquement dans votre navigateur sur :
- **http://localhost:3000**

### En parallèle

Assurez-vous que le **backend Flask** tourne sur `http://localhost:5000`.

Dans un autre terminal :
```bash
# Depuis la racine du projet QHSE
python run.py
```

## 📁 Structure du projet

```
frontend/
├── public/
│   └── index.html          # Page HTML principale
├── src/
│   ├── components/
│   │   └── Layout/
│   │       └── Layout.js   # Navigation et mise en page
│   ├── pages/
│   │   ├── Dashboard.js    # Tableau de bord
│   │   ├── DUERPList.js    # Liste des DUERP
│   │   ├── DUERPDetail.js  # Détails d'un DUERP
│   │   └── CreateDUERP.js  # Formulaire de création
│   ├── services/
│   │   └── api.js          # Appels API
│   ├── App.js              # Composant principal
│   ├── index.js            # Point d'entrée
│   └── theme.js            # Thème Material-UI
├── package.json            # Dépendances
└── README.md
```

## 🎨 Fonctionnalités

### ✅ Implémentées

- 📊 **Dashboard** - Vue d'ensemble avec statistiques
- 📋 **Liste DUERP** - Affichage de tous les DUERP avec recherche
- ➕ **Création DUERP** - Formulaire wizard step-by-step
- 👁️ **Détails DUERP** - Vue complète avec statistiques
- 📥 **Téléchargement PDF** - Génération de documents
- 🎨 **Design moderne** - Interface professionnelle Material-UI
- 📱 **Responsive** - Fonctionne sur mobile, tablette et desktop
- ✨ **Animations** - Transitions fluides avec Framer Motion

### 🔄 À venir (extensions possibles)

- 📝 Formulaires d'ajout d'unités de travail
- ⚠️ Formulaires d'ajout de risques
- 🛡️ Formulaires d'ajout de mesures de prévention
- 📊 Graphiques interactifs avancés
- 🔍 Filtres et recherche avancée
- 👥 Gestion des utilisateurs
- 🔔 Notifications
- 📱 Progressive Web App

## 🛠️ Commandes disponibles

```bash
# Démarrer en mode développement
npm start

# Créer un build de production
npm run build

# Lancer les tests
npm test

# Éjecter la configuration (⚠️ irréversible)
npm run eject
```

## 🎨 Personnalisation du thème

Le fichier `src/theme.js` contient le thème Material-UI personnalisé.

Vous pouvez modifier :
- Les couleurs (`palette`)
- La typographie (`typography`)
- Les styles des composants (`components`)

Exemple :
```javascript
primary: {
  main: '#1976d2', // Changez cette couleur
}
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `frontend` :

```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Proxy API

Le fichier `package.json` contient déjà un proxy vers le backend :

```json
"proxy": "http://localhost:5000"
```

Cela permet d'éviter les problèmes CORS en développement.

## 📱 Responsive Design

L'application est entièrement responsive et fonctionne sur :
- 📱 Mobile (< 600px)
- 📱 Tablette (600px - 960px)
- 💻 Desktop (> 960px)

## 🎯 Navigation

- `/` - Dashboard (tableau de bord)
- `/duerp` - Liste des DUERP
- `/duerp/nouveau` - Créer un nouveau DUERP
- `/duerp/:id` - Détails d'un DUERP

## 🐛 Dépannage

### Erreur "Cannot find module"

```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 déjà utilisé

Modifiez le port dans `package.json` ou utilisez :

```bash
PORT=3001 npm start
```

### Erreurs CORS

Vérifiez que :
1. Le backend est bien lancé
2. Flask-CORS est activé dans le backend
3. Le proxy est configuré dans `package.json`

### Rechargement à chaud ne fonctionne pas

```bash
# Redémarrer le serveur
# Ctrl+C puis npm start
```

## 📚 Ressources

- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [React Router Documentation](https://reactrouter.com/)
- [Framer Motion Documentation](https://www.framer.com/motion/)

## 🚀 Déploiement

### Build de production

```bash
npm run build
```

Crée un dossier `build/` optimisé pour la production.

### Servir le build

```bash
npm install -g serve
serve -s build -p 3000
```

### Déploiement sur serveur web

Copiez le contenu du dossier `build/` sur votre serveur web (Apache, Nginx, etc.).

**Configuration Nginx exemple** :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    root /path/to/build;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

## 💡 Conseils de développement

1. **Hot Reload** : Les changements se reflètent automatiquement
2. **DevTools** : Utilisez React DevTools (extension navigateur)
3. **Console** : Vérifiez la console pour les erreurs
4. **Network** : Vérifiez les appels API dans l'onglet Network

## 🎨 Captures d'écran

L'application offre :
- Design moderne et professionnel
- Interface intuitive
- Animations fluides
- Thème couleurs QHSE (bleu, vert, orange, rouge pour les risques)

## ✨ Contribution

Pour contribuer :
1. Créer une branche feature
2. Faire vos modifications
3. Tester localement
4. Créer une pull request

## 📄 Licence

MIT - Voir LICENSE dans le dossier racine
