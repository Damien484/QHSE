#!/usr/bin/env python3
"""
Script de lancement de l'application QHSE
"""
import os
import sys

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(__file__))

from backend.app import create_app

if __name__ == '__main__':
    # Obtenir le nom de l'environnement
    env = os.getenv('FLASK_ENV', 'development')

    # Créer l'application
    app = create_app(env)

    # Lancer le serveur
    print(f"🚀 Démarrage de l'application QHSE en mode {env}")
    print(f"📍 L'API est accessible sur http://localhost:5000")
    print(f"📖 Documentation: http://localhost:5000/")
    print(f"💚 Health check: http://localhost:5000/health")
    print()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(env == 'development')
    )
