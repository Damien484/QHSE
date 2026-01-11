# Guide de dépannage - Problème de base de données SQLite

Ce guide vous aide à résoudre l'erreur "unable to open database file" sur Windows.

## Diagnostic rapide

### Étape 1 : Vérifier les droits d'écriture

Dans PowerShell, dans le dossier QHSE :

```powershell
# Tester l'écriture dans le dossier database
"test" | Out-File -Encoding utf8 .\database\_test_write.txt

# Vérifier que le fichier est créé
dir .\database
```

**Résultat attendu** : Vous devez voir le fichier `_test_write.txt`

**Si le fichier n'apparaît pas** : Problème de droits. Solutions :
- Lancez PowerShell en tant qu'administrateur
- Vérifiez les permissions du dossier (clic droit > Propriétés > Sécurité)
- Déplacez le projet dans un dossier sans restrictions (comme `C:\Dev\QHSE`)

### Étape 2 : Lancer l'application avec les corrections

Les fichiers ont été corrigés pour :
- ✅ Créer automatiquement le dossier `database/` s'il n'existe pas
- ✅ Utiliser un chemin absolu compatible Windows/Linux
- ✅ Convertir les backslashes Windows en slashes pour SQLite
- ✅ Afficher le chemin exact utilisé au démarrage

Lancez l'application :

```powershell
python run.py
```

**Vous devriez voir** :

```
============================================================
CONFIGURATION DE LA BASE DE DONNÉES
============================================================
CWD (Current Working Directory) = C:\Users\qhse\Documents\QHSE
SQLALCHEMY_DATABASE_URI = sqlite:///C:/Users/qhse/Documents/QHSE/database/qhse.db
BASE_DIR calculé = C:\Users\qhse\Documents\QHSE
DATABASE_PATH = C:\Users\qhse\Documents\QHSE\database\qhse.db
Le fichier existe ? True
============================================================
```

**Si "Le fichier existe ?" = False** :
- Le fichier sera créé automatiquement au premier démarrage
- C'est normal si c'est la première fois que vous lancez l'application

### Étape 3 : Si l'erreur persiste - Forcer un chemin absolu

Créez un fichier `.env` à la racine du projet (copiez `.env.example`) :

```powershell
Copy-Item .env.example .env
```

Éditez `.env` et décommentez/modifiez la ligne `DATABASE_URL` :

```env
DATABASE_URL=sqlite:///C:/Users/qhse/Documents/QHSE/database/qhse.db
```

**ATTENTION** :
- Remplacez `qhse` par votre nom d'utilisateur Windows
- Utilisez des **slashes /** (pas de backslashes `\`)
- **3 slashes** après `sqlite:`

Pour obtenir le chemin exact :

```powershell
# Afficher le chemin complet
(Get-Location).Path
```

Copiez le résultat et remplacez les `\` par des `/`, puis ajoutez `/database/qhse.db` à la fin.

### Étape 4 : Alternative - Forcer dans PowerShell (temporaire)

Si vous ne voulez pas modifier `.env` :

```powershell
# Définir la variable d'environnement pour cette session uniquement
$env:DATABASE_URL="sqlite:///C:/Users/qhse/Documents/QHSE/database/qhse.db"

# Lancer l'application
python run.py
```

## Solutions aux problèmes courants

### Problème : "PermissionError: [Errno 13] Permission denied"

**Cause** : Antivirus, OneDrive, ou droits Windows bloquent l'accès

**Solutions** :
1. Déplacez le projet hors de OneDrive
2. Ajoutez une exception dans votre antivirus
3. Lancez PowerShell en administrateur

### Problème : "No module named 'flask_sqlalchemy'"

**Cause** : Dépendances non installées

**Solution** :
```powershell
pip install -r requirements.txt
```

### Problème : Le chemin affiché contient des backslashes

**Cause** : La conversion as_posix() n'a pas fonctionné

**Solution** : Forcer le chemin dans `.env` comme expliqué à l'Étape 3

### Problème : "database is locked"

**Cause** : Une autre instance de l'application est déjà lancée

**Solutions** :
1. Fermez toutes les fenêtres PowerShell
2. Vérifiez dans le Gestionnaire des tâches (Ctrl+Shift+Esc) qu'aucun processus Python ne tourne
3. Supprimez le fichier `database/qhse.db-journal` s'il existe
4. Relancez l'application

### Problème : Base de données vide/tables manquantes

**Solution** : Supprimer la base et la recréer

```powershell
# Supprimer l'ancienne base de données
Remove-Item .\database\qhse.db -ErrorAction SilentlyContinue

# Relancer l'application (les tables seront recréées automatiquement)
python run.py
```

## Test complet

Utilisez le script de test :

```powershell
python test_installation.py
```

Ce script vérifie :
- ✓ Version Python
- ✓ Modules installés
- ✓ Structure des fichiers
- ✓ Initialisation de la base de données

## Vérification finale

Une fois l'application lancée :

1. **Dans votre navigateur** : http://localhost:5000/health

   Vous devriez voir :
   ```json
   {
     "status": "healthy",
     "database": "connected"
   }
   ```

2. **Tester la création d'un DUERP** :

   Nouveau PowerShell :
   ```powershell
   cd C:\Users\qhse\Documents\QHSE
   .\venv\Scripts\Activate.ps1
   python docs\exemple_utilisation.py
   ```

3. **Vérifier que la base de données contient des données** :

   ```powershell
   # Installer sqlite3 (si pas déjà installé)
   # puis ouvrir la base
   sqlite3 .\database\qhse.db

   # Dans sqlite3 :
   .tables
   SELECT * FROM duerp;
   .quit
   ```

## Encore des problèmes ?

Si aucune des solutions ci-dessus ne fonctionne, collectez ces informations :

```powershell
# 1. Version Python
python --version

# 2. Chemin du projet
(Get-Location).Path

# 3. Contenu du dossier database
dir .\database

# 4. Sortie complète de l'application
python run.py 2>&1 | Out-File -Encoding utf8 debug_output.txt
```

Envoyez le contenu de `debug_output.txt` avec les informations ci-dessus.

## Astuce : Utiliser une base de données portable

Si vous voulez une base de données dans le même dossier que le projet (portable), sans chemins absolus :

Dans `.env` :

```env
# Utiliser une base de données relative au projet
DATABASE_URL=sqlite:///./database/qhse.db
```

Avec le point `.` au début du chemin, SQLite utilisera un chemin relatif depuis le répertoire où vous lancez l'application.
