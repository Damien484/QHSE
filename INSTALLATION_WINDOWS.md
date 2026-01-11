# Guide d'installation DUERP - Windows

Ce guide vous aide à installer et lancer l'application DUERP sur Windows.

## Étape 1 : Vérifier Python

Ouvrez PowerShell et vérifiez que Python est installé :

```powershell
python --version
```

Vous devez avoir Python 3.8 ou supérieur. Si ce n'est pas le cas, téléchargez Python sur https://www.python.org/downloads/

## Étape 2 : Naviguer vers le dossier du projet

```powershell
cd C:\Users\votre-nom\Documents\QHSE
```

## Étape 3 : Créer et activer l'environnement virtuel

```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1
```

**Si vous avez une erreur d'exécution de scripts**, exécutez cette commande :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayez d'activer l'environnement.

## Étape 4 : Installer les dépendances

Une fois l'environnement virtuel activé (vous devez voir `(venv)` au début de votre ligne de commande) :

```powershell
pip install -r requirements.txt
```

Cette commande va installer toutes les bibliothèques nécessaires.

## Étape 5 : Créer le fichier .env

```powershell
# Copier le fichier d'exemple
Copy-Item .env.example .env
```

## Étape 6 : Lancer l'application

```powershell
python run.py
```

Vous devriez voir :
```
🚀 Démarrage de l'application QHSE en mode development
📍 L'API est accessible sur http://localhost:5000
📖 Documentation: http://localhost:5000/
💚 Health check: http://localhost:5000/health
```

## Étape 7 : Tester l'application

### Dans votre navigateur

Ouvrez votre navigateur et allez sur :
- http://localhost:5000/ - Page d'accueil de l'API
- http://localhost:5000/health - Vérifier que l'API fonctionne

### Avec le script d'exemple

Ouvrez un **nouveau** PowerShell (gardez le premier ouvert avec l'application qui tourne) :

```powershell
# Naviguer vers le dossier
cd C:\Users\votre-nom\Documents\QHSE

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Lancer le script d'exemple
python docs\exemple_utilisation.py
```

Ce script va créer un DUERP complet avec des exemples de données.

## Étape 8 : Générer un PDF

Une fois que vous avez créé un DUERP, vous pouvez générer le PDF :

```powershell
# Utiliser curl (disponible dans PowerShell moderne)
Invoke-WebRequest -Uri "http://localhost:5000/api/duerp/1/generate" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"format":"pdf"}' `
  -OutFile "DUERP.pdf"
```

Le fichier sera sauvegardé dans votre dossier courant et aussi dans `generated_documents/`.

## Commandes utiles

### Arrêter l'application
Dans le PowerShell où l'application tourne, appuyez sur `Ctrl+C`

### Désactiver l'environnement virtuel
```powershell
deactivate
```

### Réactiver l'environnement virtuel
```powershell
.\venv\Scripts\Activate.ps1
```

### Supprimer la base de données (pour repartir de zéro)
```powershell
Remove-Item -Recurse -Force .\database\
```

## Dépannage

### Erreur "pip n'est pas reconnu"

```powershell
python -m pip install --upgrade pip
```

### Erreur lors de l'installation de reportlab

Essayez d'installer visuels C++ build tools :
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Ou installez une version pré-compilée :
```powershell
pip install --only-binary :all: reportlab
```

### L'application ne démarre pas

1. Vérifiez que l'environnement virtuel est activé (vous devez voir `(venv)`)
2. Vérifiez que toutes les dépendances sont installées : `pip list`
3. Supprimez le dossier `__pycache__` et la base de données, puis relancez

```powershell
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Remove-Item -Recurse -Force .\database\
python run.py
```

### Port 5000 déjà utilisé

Si le port 5000 est déjà utilisé, vous pouvez changer le port dans `run.py` ligne 29 :
```python
port=5001,  # Changer 5000 en 5001 ou un autre port
```

## Utilisation avec Postman ou Insomnia

Pour tester l'API avec un client REST :

1. Téléchargez Postman : https://www.postman.com/downloads/
2. Créez une nouvelle requête POST vers `http://localhost:5000/api/duerp/`
3. Dans Body, sélectionnez "raw" et "JSON"
4. Collez ceci :

```json
{
    "entreprise_nom": "Ma Société",
    "entreprise_siret": "12345678901234",
    "entreprise_adresse": "123 Rue Exemple, 75001 Paris",
    "entreprise_activite": "Fabrication",
    "effectif": 50,
    "responsable_evaluation": "Votre Nom"
}
```

5. Cliquez sur "Send"

## Support

Pour toute question, consultez :
- Le README.md principal
- La documentation dans le dossier `docs/`
- Les exemples dans `docs/exemple_utilisation.py`
