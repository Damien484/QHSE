"""
Application Flask principale pour la gestion des DUERP
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS

from app.models import db
from app.routes import duerp_bp, unite_bp, risque_bp, mesure_bp
from config.settings import config


def create_app(config_name='default'):
    """
    Factory pour créer l'application Flask

    Args:
        config_name: Nom de la configuration à utiliser (development, production, testing)

    Returns:
        Flask: Instance de l'application Flask
    """
    app = Flask(__name__)

    # Charger la configuration
    app.config.from_object(config[config_name])

    # Initialiser CORS
    CORS(app)

    # Initialiser la base de données
    db.init_app(app)

    # Créer les dossiers nécessaires
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_DOCS_FOLDER'], exist_ok=True)

    # Enregistrer les blueprints
    app.register_blueprint(duerp_bp)
    app.register_blueprint(unite_bp)
    app.register_blueprint(risque_bp)
    app.register_blueprint(mesure_bp)

    # Route racine
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API QHSE - Document Unique d\'Évaluation des Risques Professionnels',
            'version': '1.0.0',
            'endpoints': {
                'duerp': '/api/duerp',
                'unites': '/api/unite',
                'risques': '/api/risque',
                'mesures': '/api/mesure'
            }
        })

    # Route de santé
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })

    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Ressource non trouvée'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur'
        }), 500

    # Créer les tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    # Obtenir le nom de l'environnement
    env = os.getenv('FLASK_ENV', 'development')

    # Créer l'application
    app = create_app(env)

    # Lancer le serveur
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(env == 'development')
    )
