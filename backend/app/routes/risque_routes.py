"""
Routes API pour la gestion des risques
"""
from flask import request, jsonify
from . import risque_bp
from ..models import db, Risque, UniteTrail


@risque_bp.route('/', methods=['POST'])
def create_risque():
    """Crée un nouveau risque"""
    try:
        data = request.get_json()

        # Validation
        if not data.get('unite_travail_id'):
            return jsonify({
                'success': False,
                'error': 'unite_travail_id est obligatoire'
            }), 400

        if not data.get('categorie'):
            return jsonify({
                'success': False,
                'error': 'La catégorie du risque est obligatoire'
            }), 400

        if not data.get('description'):
            return jsonify({
                'success': False,
                'error': 'La description du risque est obligatoire'
            }), 400

        # Vérifier que l'unité existe
        unite = UniteTrail.query.get_or_404(data['unite_travail_id'])

        # Création du risque
        risque = Risque(
            unite_travail_id=data['unite_travail_id'],
            categorie=data['categorie'],
            sous_categorie=data.get('sous_categorie'),
            description=data['description'],
            situation_danger=data.get('situation_danger'),
            gravite=data.get('gravite', 1),
            probabilite=data.get('probabilite', 1),
            frequence_exposition=data.get('frequence_exposition'),
            personnes_exposees=data.get('personnes_exposees'),
            personnes_concernees=data.get('personnes_concernees')
        )

        db.session.add(risque)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': risque.to_dict(),
            'message': 'Risque créé avec succès'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@risque_bp.route('/<int:risque_id>', methods=['GET'])
def get_risque(risque_id):
    """Récupère un risque par son ID"""
    try:
        risque = Risque.query.get_or_404(risque_id)
        return jsonify({
            'success': True,
            'data': risque.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@risque_bp.route('/<int:risque_id>', methods=['PUT'])
def update_risque(risque_id):
    """Met à jour un risque"""
    try:
        risque = Risque.query.get_or_404(risque_id)
        data = request.get_json()

        if 'categorie' in data:
            risque.categorie = data['categorie']
        if 'sous_categorie' in data:
            risque.sous_categorie = data['sous_categorie']
        if 'description' in data:
            risque.description = data['description']
        if 'situation_danger' in data:
            risque.situation_danger = data['situation_danger']
        if 'gravite' in data:
            risque.gravite = data['gravite']
        if 'probabilite' in data:
            risque.probabilite = data['probabilite']
        if 'frequence_exposition' in data:
            risque.frequence_exposition = data['frequence_exposition']
        if 'personnes_exposees' in data:
            risque.personnes_exposees = data['personnes_exposees']
        if 'personnes_concernees' in data:
            risque.personnes_concernees = data['personnes_concernees']

        # Recalculer la criticité
        risque.calculer_criticite()

        db.session.commit()

        return jsonify({
            'success': True,
            'data': risque.to_dict(),
            'message': 'Risque mis à jour avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@risque_bp.route('/<int:risque_id>', methods=['DELETE'])
def delete_risque(risque_id):
    """Supprime un risque"""
    try:
        risque = Risque.query.get_or_404(risque_id)
        db.session.delete(risque)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Risque supprimé avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@risque_bp.route('/categories', methods=['GET'])
def get_categories():
    """Récupère la liste des catégories de risques recommandées"""
    categories = [
        {
            'nom': 'Risques mécaniques',
            'exemples': ['Chute de plain-pied', 'Chute de hauteur', 'Heurt', 'Coincement', 'Coupure', 'Écrasement']
        },
        {
            'nom': 'Risques physiques',
            'exemples': ['Bruit', 'Vibrations', 'Température', 'Éclairage', 'Rayonnements']
        },
        {
            'nom': 'Risques chimiques',
            'exemples': ['Inhalation', 'Contact cutané', 'Ingestion', 'CMR (Cancérogène, Mutagène, Reprotoxique)']
        },
        {
            'nom': 'Risques biologiques',
            'exemples': ['Virus', 'Bactéries', 'Parasites', 'Champignons']
        },
        {
            'nom': 'Risques psychosociaux',
            'exemples': ['Stress', 'Harcèlement', 'Violence', 'Charge mentale', 'Isolement']
        },
        {
            'nom': 'Risques liés à l\'activité physique',
            'exemples': ['Manutention manuelle', 'Port de charges', 'Postures pénibles', 'Gestes répétitifs']
        },
        {
            'nom': 'Risques électriques',
            'exemples': ['Électrisation', 'Électrocution', 'Brûlure électrique', 'Arc électrique']
        },
        {
            'nom': 'Risques liés aux circulations',
            'exemples': ['Circulation interne', 'Circulation externe', 'Co-activité', 'Collision']
        },
        {
            'nom': 'Risques liés à l\'incendie/explosion',
            'exemples': ['Incendie', 'Explosion', 'ATEX']
        }
    ]

    return jsonify({
        'success': True,
        'data': categories
    }), 200
