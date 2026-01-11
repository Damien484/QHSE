#!/usr/bin/env python3
"""
Script de test pour vérifier que l'installation est correcte
"""
import sys
import os

def test_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} - Version trop ancienne (3.8+ requis)")
        return False

def test_imports():
    """Vérifie que les modules nécessaires peuvent être importés"""
    print("\n🔍 Vérification des modules Python...")

    modules = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_cors', 'Flask-CORS'),
        ('reportlab', 'ReportLab'),
        ('docx', 'python-docx'),
        ('openpyxl', 'openpyxl'),
    ]

    all_ok = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"   ✓ {display_name} - OK")
        except ImportError:
            print(f"   ✗ {display_name} - MANQUANT")
            all_ok = False

    return all_ok

def test_structure():
    """Vérifie la structure des fichiers"""
    print("\n🔍 Vérification de la structure du projet...")

    required_files = [
        'backend/app.py',
        'backend/config/settings.py',
        'backend/app/models/duerp.py',
        'backend/app/routes/duerp_routes.py',
        'backend/app/services/document_generator.py',
        'requirements.txt',
        'run.py',
    ]

    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path} - OK")
        else:
            print(f"   ✗ {file_path} - MANQUANT")
            all_ok = False

    return all_ok

def test_database_init():
    """Teste l'initialisation de la base de données"""
    print("\n🔍 Test d'initialisation de la base de données...")

    try:
        # Ajouter le projet au path
        sys.path.insert(0, os.path.dirname(__file__))

        from backend.app import create_app

        app = create_app('testing')

        with app.app_context():
            from backend.app.models import db

            # Les tables sont créées automatiquement dans create_app
            print("   ✓ Base de données initialisée - OK")

            # Vérifier les tables
            from backend.app.models import DUERP, UniteTrail, Risque, MesurePrevention
            print("   ✓ Modèles chargés - OK")

        return True

    except Exception as e:
        print(f"   ✗ Erreur : {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("="*60)
    print("TEST D'INSTALLATION - Application DUERP")
    print("="*60)

    results = []

    # Tests
    results.append(("Version Python", test_python_version()))
    results.append(("Modules Python", test_imports()))
    results.append(("Structure fichiers", test_structure()))
    results.append(("Base de données", test_database_init()))

    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)

    all_passed = all(result for _, result in results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print("="*60)

    if all_passed:
        print("\n🎉 Tous les tests sont passés ! L'installation est correcte.")
        print("\nVous pouvez maintenant lancer l'application avec :")
        print("   python run.py")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Veuillez corriger les erreurs ci-dessus.")
        print("\nPour installer les dépendances manquantes :")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
