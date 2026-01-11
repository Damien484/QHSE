"""
Routes API pour la gestion des unités de travail
"""
from flask import request, jsonify
from . import unite_bp
from ..models import db, UniteTrail, DUERP


@unite_bp.route('/', methods=['POST'])
def create_unite():
    """Crée une nouvelle unité de travail"""
    try:
        data = request.get_json()

        # Validation
        if not data.get('duerp_id'):
            return jsonify({
                'success': False,
                'error': 'duerp_id est obligatoire'
            }), 400

        if not data.get('nom'):
            return jsonify({
                'success': False,
                'error': 'Le nom de l\'unité est obligatoire'
            }), 400

        # Vérifier que le DUERP existe
        duerp = DUERP.query.get_or_404(data['duerp_id'])

        # Création de l'unité
        unite = UniteTrail(
            duerp_id=data['duerp_id'],
            nom=data['nom'],
            description=data.get('description'),
            localisation=data.get('localisation'),
            nombre_employes=data.get('nombre_employes')
        )

        db.session.add(unite)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': unite.to_dict(),
            'message': 'Unité de travail créée avec succès'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@unite_bp.route('/<int:unite_id>', methods=['GET'])
def get_unite(unite_id):
    """Récupère une unité de travail par son ID"""
    try:
        unite = UniteTrail.query.get_or_404(unite_id)
        return jsonify({
            'success': True,
            'data': unite.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@unite_bp.route('/<int:unite_id>', methods=['PUT'])
def update_unite(unite_id):
    """Met à jour une unité de travail"""
    try:
        unite = UniteTrail.query.get_or_404(unite_id)
        data = request.get_json()

        if 'nom' in data:
            unite.nom = data['nom']
        if 'description' in data:
            unite.description = data['description']
        if 'localisation' in data:
            unite.localisation = data['localisation']
        if 'nombre_employes' in data:
            unite.nombre_employes = data['nombre_employes']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': unite.to_dict(),
            'message': 'Unité de travail mise à jour avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@unite_bp.route('/<int:unite_id>', methods=['DELETE'])
def delete_unite(unite_id):
    """Supprime une unité de travail"""
    try:
        unite = UniteTrail.query.get_or_404(unite_id)
        db.session.delete(unite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Unité de travail supprimée avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
