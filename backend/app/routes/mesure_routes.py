"""
Routes API pour la gestion des mesures de prévention
"""
from flask import request, jsonify
from datetime import datetime
from . import mesure_bp
from ..models import db, MesurePrevention, Risque


@mesure_bp.route('/', methods=['POST'])
def create_mesure():
    """Crée une nouvelle mesure de prévention"""
    try:
        data = request.get_json()

        # Validation
        if not data.get('risque_id'):
            return jsonify({
                'success': False,
                'error': 'risque_id est obligatoire'
            }), 400

        if not data.get('type_mesure'):
            return jsonify({
                'success': False,
                'error': 'Le type de mesure est obligatoire'
            }), 400

        if not data.get('description'):
            return jsonify({
                'success': False,
                'error': 'La description de la mesure est obligatoire'
            }), 400

        # Vérifier que le risque existe
        risque = Risque.query.get_or_404(data['risque_id'])

        # Création de la mesure
        mesure = MesurePrevention(
            risque_id=data['risque_id'],
            type_mesure=data['type_mesure'],
            niveau_hierarchie=data.get('niveau_hierarchie'),
            description=data['description'],
            statut=data.get('statut', 'planifié'),
            responsable=data.get('responsable'),
            cout_estime=data.get('cout_estime'),
            efficacite=data.get('efficacite')
        )

        # Dates
        if data.get('date_mise_en_oeuvre'):
            mesure.date_mise_en_oeuvre = datetime.fromisoformat(data['date_mise_en_oeuvre'])
        if data.get('date_echeance'):
            mesure.date_echeance = datetime.fromisoformat(data['date_echeance'])

        db.session.add(mesure)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': mesure.to_dict(),
            'message': 'Mesure de prévention créée avec succès'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@mesure_bp.route('/<int:mesure_id>', methods=['GET'])
def get_mesure(mesure_id):
    """Récupère une mesure de prévention par son ID"""
    try:
        mesure = MesurePrevention.query.get_or_404(mesure_id)
        return jsonify({
            'success': True,
            'data': mesure.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@mesure_bp.route('/<int:mesure_id>', methods=['PUT'])
def update_mesure(mesure_id):
    """Met à jour une mesure de prévention"""
    try:
        mesure = MesurePrevention.query.get_or_404(mesure_id)
        data = request.get_json()

        if 'type_mesure' in data:
            mesure.type_mesure = data['type_mesure']
        if 'niveau_hierarchie' in data:
            mesure.niveau_hierarchie = data['niveau_hierarchie']
        if 'description' in data:
            mesure.description = data['description']
        if 'statut' in data:
            mesure.statut = data['statut']
        if 'responsable' in data:
            mesure.responsable = data['responsable']
        if 'cout_estime' in data:
            mesure.cout_estime = data['cout_estime']
        if 'efficacite' in data:
            mesure.efficacite = data['efficacite']

        # Dates
        if 'date_mise_en_oeuvre' in data:
            mesure.date_mise_en_oeuvre = datetime.fromisoformat(data['date_mise_en_oeuvre']) if data['date_mise_en_oeuvre'] else None
        if 'date_echeance' in data:
            mesure.date_echeance = datetime.fromisoformat(data['date_echeance']) if data['date_echeance'] else None

        db.session.commit()

        return jsonify({
            'success': True,
            'data': mesure.to_dict(),
            'message': 'Mesure de prévention mise à jour avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@mesure_bp.route('/<int:mesure_id>', methods=['DELETE'])
def delete_mesure(mesure_id):
    """Supprime une mesure de prévention"""
    try:
        mesure = MesurePrevention.query.get_or_404(mesure_id)
        db.session.delete(mesure)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Mesure de prévention supprimée avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@mesure_bp.route('/types', methods=['GET'])
def get_types_mesures():
    """Récupère la liste des types de mesures selon la hiérarchie de prévention"""
    types_mesures = [
        {
            'niveau': 1,
            'type': 'Suppression du risque',
            'description': 'Éliminer complètement le danger'
        },
        {
            'niveau': 2,
            'type': 'Substitution',
            'description': 'Remplacer ce qui est dangereux par ce qui ne l\'est pas ou moins'
        },
        {
            'niveau': 3,
            'type': 'Protection collective',
            'description': 'Mesures techniques de protection collective (garde-corps, ventilation, etc.)'
        },
        {
            'niveau': 4,
            'type': 'Organisation du travail',
            'description': 'Mesures organisationnelles (procédures, formation, rotation, etc.)'
        },
        {
            'niveau': 5,
            'type': 'Protection individuelle',
            'description': 'Équipements de protection individuelle (EPI)'
        }
    ]

    return jsonify({
        'success': True,
        'data': types_mesures
    }), 200
