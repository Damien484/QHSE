"""
Script d'exemple pour utiliser l'API DUERP
Ce script montre comment créer un DUERP complet via l'API
"""
import requests
import json
from datetime import datetime, date

# URL de base de l'API
BASE_URL = 'http://localhost:5000/api'


def create_duerp_example():
    """Crée un exemple complet de DUERP"""

    print("=" * 80)
    print("EXEMPLE DE CRÉATION D'UN DUERP")
    print("=" * 80)
    print()

    # 1. Créer le DUERP
    print("1. Création du DUERP...")
    duerp_data = {
        "entreprise_nom": "Entreprise Exemple SA",
        "entreprise_siret": "12345678901234",
        "entreprise_adresse": "123 Rue de la Sécurité, 75001 Paris",
        "entreprise_activite": "Fabrication de composants électroniques",
        "effectif": 50,
        "version": "1.0",
        "responsable_evaluation": "Jean Dupont - Responsable QHSE",
        "responsable_validation": "Marie Martin - Directrice"
    }

    response = requests.post(f'{BASE_URL}/duerp/', json=duerp_data)
    if response.status_code == 201:
        duerp = response.json()['data']
        duerp_id = duerp['id']
        print(f"✓ DUERP créé avec l'ID: {duerp_id}")
        print(f"  Entreprise: {duerp['entreprise_nom']}")
        print(f"  Version: {duerp['version']}")
    else:
        print(f"✗ Erreur lors de la création du DUERP: {response.text}")
        return

    print()

    # 2. Créer des unités de travail
    print("2. Création des unités de travail...")

    unites = [
        {
            "duerp_id": duerp_id,
            "nom": "Atelier de production",
            "description": "Zone de fabrication et assemblage des composants",
            "localisation": "Bâtiment A - Rez-de-chaussée",
            "nombre_employes": 25
        },
        {
            "duerp_id": duerp_id,
            "nom": "Bureau d'études",
            "description": "Conception et développement de nouveaux produits",
            "localisation": "Bâtiment B - 1er étage",
            "nombre_employes": 15
        },
        {
            "duerp_id": duerp_id,
            "nom": "Entrepôt logistique",
            "description": "Stockage et expédition des produits finis",
            "localisation": "Bâtiment C",
            "nombre_employes": 10
        }
    ]

    unite_ids = []
    for unite_data in unites:
        response = requests.post(f'{BASE_URL}/unite/', json=unite_data)
        if response.status_code == 201:
            unite = response.json()['data']
            unite_ids.append(unite['id'])
            print(f"✓ Unité créée: {unite['nom']} (ID: {unite['id']})")
        else:
            print(f"✗ Erreur: {response.text}")

    print()

    # 3. Créer des risques pour l'atelier de production
    print("3. Création des risques pour l'atelier de production...")

    risques_atelier = [
        {
            "unite_travail_id": unite_ids[0],
            "categorie": "Risques mécaniques",
            "sous_categorie": "Coupure",
            "description": "Risque de coupure lors de la manipulation de pièces métalliques",
            "situation_danger": "Manipulation de tôles et pièces coupantes sans protection",
            "gravite": 3,
            "probabilite": 3,
            "frequence_exposition": "Permanente",
            "personnes_exposees": 15,
            "personnes_concernees": "Opérateurs de production"
        },
        {
            "unite_travail_id": unite_ids[0],
            "categorie": "Risques chimiques",
            "sous_categorie": "Inhalation",
            "description": "Exposition aux vapeurs de solvants lors du nettoyage des pièces",
            "situation_danger": "Utilisation de solvants dans un espace confiné",
            "gravite": 4,
            "probabilite": 2,
            "frequence_exposition": "Fréquente",
            "personnes_exposees": 8,
            "personnes_concernees": "Personnel de nettoyage et finition"
        },
        {
            "unite_travail_id": unite_ids[0],
            "categorie": "Risques physiques",
            "sous_categorie": "Bruit",
            "description": "Exposition au bruit des machines de production",
            "situation_danger": "Niveau sonore supérieur à 85 dB pendant plusieurs heures",
            "gravite": 2,
            "probabilite": 4,
            "frequence_exposition": "Permanente",
            "personnes_exposees": 20,
            "personnes_concernees": "Ensemble du personnel de l'atelier"
        }
    ]

    risque_ids = []
    for risque_data in risques_atelier:
        response = requests.post(f'{BASE_URL}/risque/', json=risque_data)
        if response.status_code == 201:
            risque = response.json()['data']
            risque_ids.append(risque['id'])
            print(f"✓ Risque créé: {risque['categorie']}")
            print(f"  Criticité: {risque['criticite']} - Niveau: {risque['niveau_risque']}")
        else:
            print(f"✗ Erreur: {response.text}")

    print()

    # 4. Créer des mesures de prévention
    print("4. Création des mesures de prévention...")

    mesures = [
        {
            "risque_id": risque_ids[0],  # Risque de coupure
            "type_mesure": "Protection collective",
            "niveau_hierarchie": 3,
            "description": "Installation de protections sur les machines et outils coupants",
            "statut": "réalisé",
            "responsable": "Chef d'atelier",
            "efficacite": "Bonne"
        },
        {
            "risque_id": risque_ids[0],
            "type_mesure": "Protection individuelle",
            "niveau_hierarchie": 5,
            "description": "Port obligatoire de gants anti-coupure",
            "statut": "réalisé",
            "responsable": "Responsable QHSE",
            "efficacite": "Moyenne"
        },
        {
            "risque_id": risque_ids[1],  # Risque chimique
            "type_mesure": "Substitution",
            "niveau_hierarchie": 2,
            "description": "Remplacer les solvants par des produits moins toxiques",
            "statut": "en_cours",
            "responsable": "Bureau d'études",
            "cout_estime": 5000.0,
            "efficacite": "Excellente"
        },
        {
            "risque_id": risque_ids[1],
            "type_mesure": "Protection collective",
            "niveau_hierarchie": 3,
            "description": "Installation d'un système de ventilation locale",
            "statut": "planifié",
            "responsable": "Services techniques",
            "cout_estime": 15000.0
        },
        {
            "risque_id": risque_ids[2],  # Risque bruit
            "type_mesure": "Protection collective",
            "niveau_hierarchie": 3,
            "description": "Isolation phonique des machines les plus bruyantes",
            "statut": "planifié",
            "responsable": "Direction",
            "cout_estime": 25000.0
        },
        {
            "risque_id": risque_ids[2],
            "type_mesure": "Protection individuelle",
            "niveau_hierarchie": 5,
            "description": "Port obligatoire de protections auditives",
            "statut": "réalisé",
            "responsable": "Chef d'atelier",
            "efficacite": "Bonne"
        }
    ]

    for mesure_data in mesures:
        response = requests.post(f'{BASE_URL}/mesure/', json=mesure_data)
        if response.status_code == 201:
            mesure = response.json()['data']
            print(f"✓ Mesure créée: {mesure['type_mesure']}")
            print(f"  Statut: {mesure['statut']}")
        else:
            print(f"✗ Erreur: {response.text}")

    print()

    # 5. Obtenir les statistiques
    print("5. Statistiques du DUERP...")
    response = requests.get(f'{BASE_URL}/duerp/{duerp_id}/stats')
    if response.status_code == 200:
        stats = response.json()['data']
        print(f"✓ Statistiques:")
        print(f"  Nombre d'unités: {stats['nombre_unites']}")
        print(f"  Nombre total de risques: {stats['nombre_risques_total']}")
        print(f"  Risques critiques: {stats['nombre_risques_par_niveau']['Critique']}")
        print(f"  Risques importants: {stats['nombre_risques_par_niveau']['Important']}")
        print(f"  Risques modérés: {stats['nombre_risques_par_niveau']['Modéré']}")
        print(f"  Risques acceptables: {stats['nombre_risques_par_niveau']['Acceptable']}")
        print(f"  Nombre de mesures de prévention: {stats['nombre_mesures_prevention']}")
    else:
        print(f"✗ Erreur: {response.text}")

    print()

    # 6. Valider le DUERP
    print("6. Validation du DUERP...")
    response = requests.post(
        f'{BASE_URL}/duerp/{duerp_id}/validate',
        json={"validateur": "Marie Martin - Directrice"}
    )
    if response.status_code == 200:
        print(f"✓ DUERP validé avec succès")
    else:
        print(f"✗ Erreur: {response.text}")

    print()

    # 7. Générer le document PDF
    print("7. Génération du document PDF...")
    print("  (Envoyer une requête POST à /api/duerp/{duerp_id}/generate avec format='pdf')")
    print(f"  URL: {BASE_URL}/duerp/{duerp_id}/generate")
    print()

    print("=" * 80)
    print(f"✓ DUERP créé avec succès ! ID: {duerp_id}")
    print("=" * 80)
    print()
    print("Pour récupérer le DUERP complet:")
    print(f"  GET {BASE_URL}/duerp/{duerp_id}")
    print()
    print("Pour générer le document PDF:")
    print(f"  POST {BASE_URL}/duerp/{duerp_id}/generate")
    print('  Body: {"format": "pdf"}')
    print()

    return duerp_id


if __name__ == '__main__':
    try:
        # Vérifier que l'API est accessible
        response = requests.get(f'{BASE_URL.replace("/api", "")}/health')
        if response.status_code != 200:
            print("⚠️  L'API n'est pas accessible. Assurez-vous qu'elle est démarrée.")
            print("   Lancez l'API avec: python run.py")
            exit(1)

        # Créer l'exemple
        create_duerp_example()

    except requests.exceptions.ConnectionError:
        print("⚠️  Impossible de se connecter à l'API.")
        print("   Assurez-vous que l'API est démarrée avec: python run.py")
        exit(1)
