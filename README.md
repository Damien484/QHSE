# QHSE - Gestion des DUERP

Application de gestion du Document Unique d'Évaluation des Risques Professionnels (DUERP) conforme à la réglementation française.

## Description

Cette application permet de créer, gérer et générer des Documents Uniques d'Évaluation des Risques Professionnels (DUERP) conformes aux exigences du Code du travail français (Articles L4121-1 à L4121-5 et R4121-1 à R4121-4).

### Fonctionnalités principales

- Création et gestion de DUERP
- Gestion des unités de travail
- Identification et évaluation des risques professionnels
- Cotation automatique des risques (Gravité × Probabilité)
- Gestion des mesures de prévention selon la hiérarchie réglementaire
- Génération de documents PDF et DOCX
- Suivi historique des évaluations
- Statistiques et tableaux de bord
- API RESTful complète

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone <url-du-depot>
cd QHSE
```

2. Créer un environnement virtuel :
```bash
python -m venv venv

# Sur Linux/Mac
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer le fichier .env avec vos paramètres
```

5. Lancer l'application :
```bash
python run.py
```

L'API sera accessible sur `http://localhost:5000`

## Structure du projet

```
QHSE/
├── backend/
│   ├── app/
│   │   ├── models/          # Modèles de données SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   └── duerp.py     # Modèles DUERP, Risque, Mesure, etc.
│   │   ├── routes/          # Routes API REST
│   │   │   ├── __init__.py
│   │   │   ├── duerp_routes.py
│   │   │   ├── unite_routes.py
│   │   │   ├── risque_routes.py
│   │   │   └── mesure_routes.py
│   │   ├── services/        # Logique métier
│   │   │   ├── __init__.py
│   │   │   └── document_generator.py
│   │   └── templates/       # Templates de documents
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Configuration de l'application
│   └── app.py               # Application Flask principale
├── database/                # Base de données SQLite
├── docs/                    # Documentation
│   └── exemple_utilisation.py
├── generated_documents/     # Documents générés (PDF, DOCX)
├── tests/                   # Tests unitaires
├── .env.example             # Exemple de configuration
├── .gitignore
├── requirements.txt         # Dépendances Python
├── run.py                   # Script de lancement
└── README.md

```

## API REST

### Endpoints principaux

#### DUERP

- `GET /api/duerp/` - Liste tous les DUERP
- `POST /api/duerp/` - Crée un nouveau DUERP
- `GET /api/duerp/{id}` - Récupère un DUERP spécifique
- `PUT /api/duerp/{id}` - Met à jour un DUERP
- `DELETE /api/duerp/{id}` - Supprime un DUERP
- `POST /api/duerp/{id}/validate` - Valide un DUERP
- `POST /api/duerp/{id}/generate` - Génère le document PDF/DOCX
- `GET /api/duerp/{id}/stats` - Obtient les statistiques
- `GET /api/duerp/{id}/history` - Obtient l'historique

#### Unités de travail

- `POST /api/unite/` - Crée une unité de travail
- `GET /api/unite/{id}` - Récupère une unité
- `PUT /api/unite/{id}` - Met à jour une unité
- `DELETE /api/unite/{id}` - Supprime une unité

#### Risques

- `POST /api/risque/` - Crée un risque
- `GET /api/risque/{id}` - Récupère un risque
- `PUT /api/risque/{id}` - Met à jour un risque
- `DELETE /api/risque/{id}` - Supprime un risque
- `GET /api/risque/categories` - Liste les catégories de risques

#### Mesures de prévention

- `POST /api/mesure/` - Crée une mesure de prévention
- `GET /api/mesure/{id}` - Récupère une mesure
- `PUT /api/mesure/{id}` - Met à jour une mesure
- `DELETE /api/mesure/{id}` - Supprime une mesure
- `GET /api/mesure/types` - Liste les types de mesures

## Utilisation

### Exemple de création d'un DUERP

```python
import requests

# 1. Créer un DUERP
duerp_data = {
    "entreprise_nom": "Mon Entreprise",
    "entreprise_siret": "12345678901234",
    "entreprise_adresse": "123 Rue Exemple, 75001 Paris",
    "entreprise_activite": "Fabrication",
    "effectif": 50,
    "responsable_evaluation": "Jean Dupont"
}

response = requests.post('http://localhost:5000/api/duerp/', json=duerp_data)
duerp = response.json()['data']
duerp_id = duerp['id']

# 2. Créer une unité de travail
unite_data = {
    "duerp_id": duerp_id,
    "nom": "Atelier de production",
    "description": "Zone de fabrication",
    "nombre_employes": 25
}

response = requests.post('http://localhost:5000/api/unite/', json=unite_data)
unite = response.json()['data']

# 3. Créer un risque
risque_data = {
    "unite_travail_id": unite['id'],
    "categorie": "Risques mécaniques",
    "description": "Risque de coupure",
    "gravite": 3,
    "probabilite": 2
}

response = requests.post('http://localhost:5000/api/risque/', json=risque_data)
risque = response.json()['data']

# 4. Créer une mesure de prévention
mesure_data = {
    "risque_id": risque['id'],
    "type_mesure": "Protection collective",
    "description": "Installation de protections sur les machines",
    "statut": "planifié"
}

response = requests.post('http://localhost:5000/api/mesure/', json=mesure_data)

# 5. Générer le document PDF
response = requests.post(
    f'http://localhost:5000/api/duerp/{duerp_id}/generate',
    json={"format": "pdf"}
)
```

Un exemple complet est disponible dans `docs/exemple_utilisation.py`.

Pour l'exécuter :
```bash
python docs/exemple_utilisation.py
```

## Méthodologie d'évaluation des risques

### Cotation des risques

La criticité d'un risque est calculée automatiquement selon la formule :

**Criticité = Gravité × Probabilité**

#### Échelle de Gravité (G)
- 1 = Mineure (blessure sans arrêt de travail)
- 2 = Moyenne (arrêt de travail temporaire)
- 3 = Grave (incapacité permanente partielle)
- 4 = Très grave (décès ou incapacité permanente totale)

#### Échelle de Probabilité (P)
- 1 = Très improbable (moins d'une fois tous les 10 ans)
- 2 = Improbable (une fois tous les 1 à 10 ans)
- 3 = Probable (plusieurs fois par an)
- 4 = Très probable (plusieurs fois par mois)

#### Niveaux de risque
- **Acceptable (1-2)** : Risque faible, surveillance normale
- **Modéré (3-6)** : Risque modéré, actions de prévention à planifier
- **Important (8-12)** : Risque important, actions de prévention prioritaires
- **Critique (16)** : Risque critique, actions immédiates requises

### Hiérarchie des mesures de prévention

Selon le Code du travail, les mesures de prévention doivent suivre cet ordre de priorité :

1. **Suppression du risque** (niveau 1) - Éliminer complètement le danger
2. **Substitution** (niveau 2) - Remplacer ce qui est dangereux
3. **Protection collective** (niveau 3) - Mesures techniques collectives
4. **Organisation du travail** (niveau 4) - Mesures organisationnelles
5. **Protection individuelle** (niveau 5) - Équipements de protection (EPI)

## Catégories de risques

L'application supporte les catégories de risques suivantes :

- **Risques mécaniques** : Chute, heurt, coupure, écrasement, etc.
- **Risques physiques** : Bruit, vibrations, température, rayonnements
- **Risques chimiques** : Inhalation, contact cutané, CMR
- **Risques biologiques** : Virus, bactéries, parasites
- **Risques psychosociaux** : Stress, harcèlement, charge mentale
- **Risques liés à l'activité physique** : Manutention, postures pénibles
- **Risques électriques** : Électrisation, électrocution
- **Risques liés aux circulations** : Circulation interne/externe
- **Risques incendie/explosion** : Incendie, explosion, ATEX

## Conformité réglementaire

Cette application est conçue pour être conforme aux exigences du Code du travail français :

- **Articles L4121-1 à L4121-5** : Obligations de l'employeur
- **Articles R4121-1 à R4121-4** : Évaluation des risques
- Traçabilité des évaluations (historique)
- Mise à jour au moins annuelle
- Accessibilité aux travailleurs et instances représentatives

## Génération de documents

L'application génère des documents professionnels au format :
- **PDF** : Document officiel avec mise en page complète
- **DOCX** : Document éditable Microsoft Word

Les documents générés incluent :
- Page de garde avec informations de l'entreprise
- Contexte réglementaire
- Méthodologie d'évaluation
- Tableaux récapitulatifs des risques
- Évaluation détaillée par unité de travail
- Mesures de prévention associées

## Développement

### Lancer en mode développement

```bash
export FLASK_ENV=development
python run.py
```

### Tests

```bash
# À venir
pytest tests/
```

## Technologies utilisées

- **Backend** : Flask (Python)
- **Base de données** : SQLAlchemy avec SQLite
- **Génération PDF** : ReportLab
- **Génération DOCX** : python-docx
- **API REST** : Flask-RESTful
- **CORS** : Flask-CORS

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur le dépôt GitHub.

## Roadmap

- [ ] Interface web (frontend)
- [ ] Export Excel
- [ ] Gestion des utilisateurs et authentification
- [ ] Notifications et rappels d'évaluation
- [ ] Intégration avec d'autres outils QHSE
- [ ] Tableaux de bord avancés
- [ ] API mobile