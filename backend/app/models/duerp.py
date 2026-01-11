"""
Modèles de données pour le DUERP (Document Unique d'Évaluation des Risques Professionnels)
"""
from datetime import datetime
from . import db


class DUERP(db.Model):
    """
    Document Unique d'Évaluation des Risques Professionnels
    Représente le document principal conforme à la réglementation française
    """
    __tablename__ = 'duerp'

    id = db.Column(db.Integer, primary_key=True)
    entreprise_nom = db.Column(db.String(200), nullable=False)
    entreprise_siret = db.Column(db.String(14))
    entreprise_adresse = db.Column(db.Text)
    entreprise_activite = db.Column(db.String(200))
    effectif = db.Column(db.Integer)

    # Informations sur le document
    version = db.Column(db.String(20), nullable=False, default='1.0')
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_derniere_maj = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_prochaine_evaluation = db.Column(db.Date)

    # Responsables
    responsable_evaluation = db.Column(db.String(100))
    responsable_validation = db.Column(db.String(100))

    # Statut du document
    statut = db.Column(db.String(20), default='brouillon')  # brouillon, validé, archivé

    # Relations
    unites_travail = db.relationship('UniteTrail', backref='duerp', lazy=True, cascade='all, delete-orphan')
    historique = db.relationship('EvaluationHistorique', backref='duerp', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<DUERP {self.entreprise_nom} - v{self.version}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'entreprise_nom': self.entreprise_nom,
            'entreprise_siret': self.entreprise_siret,
            'entreprise_adresse': self.entreprise_adresse,
            'entreprise_activite': self.entreprise_activite,
            'effectif': self.effectif,
            'version': self.version,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_derniere_maj': self.date_derniere_maj.isoformat() if self.date_derniere_maj else None,
            'date_prochaine_evaluation': self.date_prochaine_evaluation.isoformat() if self.date_prochaine_evaluation else None,
            'responsable_evaluation': self.responsable_evaluation,
            'responsable_validation': self.responsable_validation,
            'statut': self.statut,
            'unites_travail': [unite.to_dict() for unite in self.unites_travail]
        }


class UniteTrail(db.Model):
    """
    Unité de travail (service, atelier, poste, etc.)
    """
    __tablename__ = 'unite_travail'

    id = db.Column(db.Integer, primary_key=True)
    duerp_id = db.Column(db.Integer, db.ForeignKey('duerp.id'), nullable=False)

    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    localisation = db.Column(db.String(200))
    nombre_employes = db.Column(db.Integer)

    # Relations
    risques = db.relationship('Risque', backref='unite_travail', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<UniteTrail {self.nom}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'localisation': self.localisation,
            'nombre_employes': self.nombre_employes,
            'risques': [risque.to_dict() for risque in self.risques]
        }


class Risque(db.Model):
    """
    Risque professionnel identifié dans une unité de travail
    """
    __tablename__ = 'risque'

    id = db.Column(db.Integer, primary_key=True)
    unite_travail_id = db.Column(db.Integer, db.ForeignKey('unite_travail.id'), nullable=False)

    # Classification du risque
    categorie = db.Column(db.String(100), nullable=False)  # Mécanique, Chimique, Biologique, Psychosocial, etc.
    sous_categorie = db.Column(db.String(100))

    # Description
    description = db.Column(db.Text, nullable=False)
    situation_danger = db.Column(db.Text)

    # Évaluation du risque
    gravite = db.Column(db.Integer, nullable=False)  # 1 (faible) à 4 (très grave)
    probabilite = db.Column(db.Integer, nullable=False)  # 1 (très improbable) à 4 (très probable)
    frequence_exposition = db.Column(db.String(50))  # Permanente, Fréquente, Occasionnelle, Rare

    # Criticité calculée
    criticite = db.Column(db.Integer)  # gravité × probabilité
    niveau_risque = db.Column(db.String(20))  # Acceptable, Modéré, Important, Critique

    # Population exposée
    personnes_exposees = db.Column(db.Integer)
    personnes_concernees = db.Column(db.Text)  # Description des personnes exposées

    # Relations
    mesures_prevention = db.relationship('MesurePrevention', backref='risque', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(Risque, self).__init__(**kwargs)
        self.calculer_criticite()

    def calculer_criticite(self):
        """Calcule la criticité et le niveau de risque"""
        if self.gravite and self.probabilite:
            self.criticite = self.gravite * self.probabilite

            # Détermination du niveau de risque
            if self.criticite <= 2:
                self.niveau_risque = 'Acceptable'
            elif self.criticite <= 6:
                self.niveau_risque = 'Modéré'
            elif self.criticite <= 12:
                self.niveau_risque = 'Important'
            else:
                self.niveau_risque = 'Critique'

    def __repr__(self):
        return f'<Risque {self.categorie} - Criticité: {self.criticite}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'categorie': self.categorie,
            'sous_categorie': self.sous_categorie,
            'description': self.description,
            'situation_danger': self.situation_danger,
            'gravite': self.gravite,
            'probabilite': self.probabilite,
            'frequence_exposition': self.frequence_exposition,
            'criticite': self.criticite,
            'niveau_risque': self.niveau_risque,
            'personnes_exposees': self.personnes_exposees,
            'personnes_concernees': self.personnes_concernees,
            'mesures_prevention': [mesure.to_dict() for mesure in self.mesures_prevention]
        }


class MesurePrevention(db.Model):
    """
    Mesure de prévention associée à un risque
    """
    __tablename__ = 'mesure_prevention'

    id = db.Column(db.Integer, primary_key=True)
    risque_id = db.Column(db.Integer, db.ForeignKey('risque.id'), nullable=False)

    # Type de mesure selon la hiérarchie de prévention
    type_mesure = db.Column(db.String(50), nullable=False)  # Suppression, Substitution, Collective, Individuelle, etc.
    niveau_hierarchie = db.Column(db.Integer)  # 1 (meilleure) à 5 (moins efficace)

    description = db.Column(db.Text, nullable=False)

    # Statut de mise en œuvre
    statut = db.Column(db.String(20), default='planifié')  # planifié, en_cours, réalisé
    date_mise_en_oeuvre = db.Column(db.Date)
    date_echeance = db.Column(db.Date)

    # Responsabilités
    responsable = db.Column(db.String(100))
    cout_estime = db.Column(db.Float)

    # Efficacité
    efficacite = db.Column(db.String(20))  # Faible, Moyenne, Bonne, Excellente

    def __repr__(self):
        return f'<MesurePrevention {self.type_mesure} - {self.statut}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'type_mesure': self.type_mesure,
            'niveau_hierarchie': self.niveau_hierarchie,
            'description': self.description,
            'statut': self.statut,
            'date_mise_en_oeuvre': self.date_mise_en_oeuvre.isoformat() if self.date_mise_en_oeuvre else None,
            'date_echeance': self.date_echeance.isoformat() if self.date_echeance else None,
            'responsable': self.responsable,
            'cout_estime': self.cout_estime,
            'efficacite': self.efficacite
        }


class EvaluationHistorique(db.Model):
    """
    Historique des évaluations et modifications du DUERP
    Traçabilité réglementaire
    """
    __tablename__ = 'evaluation_historique'

    id = db.Column(db.Integer, primary_key=True)
    duerp_id = db.Column(db.Integer, db.ForeignKey('duerp.id'), nullable=False)

    date_evaluation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    version = db.Column(db.String(20), nullable=False)
    type_modification = db.Column(db.String(50))  # Création, Mise à jour, Réévaluation complète

    description_modifications = db.Column(db.Text)
    evaluateur = db.Column(db.String(100))

    # Indicateurs globaux à cette date
    nombre_risques_total = db.Column(db.Integer)
    nombre_risques_critiques = db.Column(db.Integer)
    nombre_mesures_prevention = db.Column(db.Integer)

    def __repr__(self):
        return f'<EvaluationHistorique v{self.version} - {self.date_evaluation}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'date_evaluation': self.date_evaluation.isoformat() if self.date_evaluation else None,
            'version': self.version,
            'type_modification': self.type_modification,
            'description_modifications': self.description_modifications,
            'evaluateur': self.evaluateur,
            'nombre_risques_total': self.nombre_risques_total,
            'nombre_risques_critiques': self.nombre_risques_critiques,
            'nombre_mesures_prevention': self.nombre_mesures_prevention
        }
