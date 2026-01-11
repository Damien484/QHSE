"""
Routes API pour la gestion des DUERP
"""
from flask import request, jsonify, send_file
from datetime import datetime
from . import duerp_bp
from ..models import db, DUERP, EvaluationHistorique
from ..services.document_generator import DUERPDocumentGenerator


@duerp_bp.route('/', methods=['GET'])
def get_all_duerp():
    """Récupère tous les DUERP"""
    try:
        duerps = DUERP.query.all()
        return jsonify({
            'success': True,
            'data': [duerp.to_dict() for duerp in duerps]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>', methods=['GET'])
def get_duerp(duerp_id):
    """Récupère un DUERP spécifique par son ID"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)
        return jsonify({
            'success': True,
            'data': duerp.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@duerp_bp.route('/', methods=['POST'])
def create_duerp():
    """Crée un nouveau DUERP"""
    try:
        data = request.get_json()

        # Validation des données obligatoires
        if not data.get('entreprise_nom'):
            return jsonify({
                'success': False,
                'error': 'Le nom de l\'entreprise est obligatoire'
            }), 400

        # Création du DUERP
        duerp = DUERP(
            entreprise_nom=data.get('entreprise_nom'),
            entreprise_siret=data.get('entreprise_siret'),
            entreprise_adresse=data.get('entreprise_adresse'),
            entreprise_activite=data.get('entreprise_activite'),
            effectif=data.get('effectif'),
            version=data.get('version', '1.0'),
            responsable_evaluation=data.get('responsable_evaluation'),
            responsable_validation=data.get('responsable_validation'),
            statut='brouillon'
        )

        db.session.add(duerp)
        db.session.commit()

        # Créer une entrée dans l'historique
        historique = EvaluationHistorique(
            duerp_id=duerp.id,
            version=duerp.version,
            type_modification='Création',
            description_modifications='Création initiale du DUERP',
            evaluateur=data.get('responsable_evaluation', 'Non spécifié'),
            nombre_risques_total=0,
            nombre_risques_critiques=0,
            nombre_mesures_prevention=0
        )
        db.session.add(historique)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': duerp.to_dict(),
            'message': 'DUERP créé avec succès'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>', methods=['PUT'])
def update_duerp(duerp_id):
    """Met à jour un DUERP existant"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)
        data = request.get_json()

        # Mise à jour des champs
        if 'entreprise_nom' in data:
            duerp.entreprise_nom = data['entreprise_nom']
        if 'entreprise_siret' in data:
            duerp.entreprise_siret = data['entreprise_siret']
        if 'entreprise_adresse' in data:
            duerp.entreprise_adresse = data['entreprise_adresse']
        if 'entreprise_activite' in data:
            duerp.entreprise_activite = data['entreprise_activite']
        if 'effectif' in data:
            duerp.effectif = data['effectif']
        if 'responsable_evaluation' in data:
            duerp.responsable_evaluation = data['responsable_evaluation']
        if 'responsable_validation' in data:
            duerp.responsable_validation = data['responsable_validation']
        if 'statut' in data:
            duerp.statut = data['statut']

        duerp.date_derniere_maj = datetime.utcnow()

        # Créer une entrée dans l'historique
        if data.get('create_history', True):
            historique = EvaluationHistorique(
                duerp_id=duerp.id,
                version=duerp.version,
                type_modification='Mise à jour',
                description_modifications=data.get('description_modifications', 'Mise à jour des informations'),
                evaluateur=data.get('evaluateur', duerp.responsable_evaluation)
            )
            db.session.add(historique)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': duerp.to_dict(),
            'message': 'DUERP mis à jour avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>', methods=['DELETE'])
def delete_duerp(duerp_id):
    """Supprime un DUERP"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)
        db.session.delete(duerp)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'DUERP supprimé avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>/validate', methods=['POST'])
def validate_duerp(duerp_id):
    """Valide un DUERP (passage du statut brouillon à validé)"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)
        data = request.get_json()

        duerp.statut = 'validé'
        duerp.date_derniere_maj = datetime.utcnow()

        # Créer une entrée dans l'historique
        historique = EvaluationHistorique(
            duerp_id=duerp.id,
            version=duerp.version,
            type_modification='Validation',
            description_modifications='Validation du DUERP',
            evaluateur=data.get('validateur', duerp.responsable_validation)
        )
        db.session.add(historique)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': duerp.to_dict(),
            'message': 'DUERP validé avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>/generate', methods=['POST'])
def generate_document(duerp_id):
    """Génère le document DUERP au format PDF"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)
        data = request.get_json() or {}
        format_type = data.get('format', 'pdf')  # pdf ou docx

        generator = DUERPDocumentGenerator()

        if format_type == 'pdf':
            file_path = generator.generate_pdf(duerp)
        elif format_type == 'docx':
            file_path = generator.generate_docx(duerp)
        else:
            return jsonify({
                'success': False,
                'error': 'Format non supporté. Utilisez "pdf" ou "docx"'
            }), 400

        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'DUERP_{duerp.entreprise_nom}_{duerp.version}.{format_type}'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>/stats', methods=['GET'])
def get_duerp_stats(duerp_id):
    """Récupère les statistiques d'un DUERP"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)

        # Calcul des statistiques
        stats = {
            'nombre_unites': len(duerp.unites_travail),
            'nombre_risques_total': 0,
            'nombre_risques_par_niveau': {
                'Acceptable': 0,
                'Modéré': 0,
                'Important': 0,
                'Critique': 0
            },
            'nombre_mesures_prevention': 0,
            'mesures_par_statut': {
                'planifié': 0,
                'en_cours': 0,
                'réalisé': 0
            },
            'risques_par_categorie': {}
        }

        for unite in duerp.unites_travail:
            for risque in unite.risques:
                stats['nombre_risques_total'] += 1
                stats['nombre_risques_par_niveau'][risque.niveau_risque] += 1

                # Comptage par catégorie
                if risque.categorie not in stats['risques_par_categorie']:
                    stats['risques_par_categorie'][risque.categorie] = 0
                stats['risques_par_categorie'][risque.categorie] += 1

                # Comptage des mesures
                for mesure in risque.mesures_prevention:
                    stats['nombre_mesures_prevention'] += 1
                    stats['mesures_par_statut'][mesure.statut] += 1

        return jsonify({
            'success': True,
            'data': stats
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@duerp_bp.route('/<int:duerp_id>/history', methods=['GET'])
def get_duerp_history(duerp_id):
    """Récupère l'historique des modifications d'un DUERP"""
    try:
        duerp = DUERP.query.get_or_404(duerp_id)

        return jsonify({
            'success': True,
            'data': [h.to_dict() for h in duerp.historique]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
