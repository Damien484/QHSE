"""
Database models for QHSE application
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models
from .duerp import DUERP, UniteTrail, Risque, MesurePrevention, EvaluationHistorique

__all__ = ['db', 'DUERP', 'UniteTrail', 'Risque', 'MesurePrevention', 'EvaluationHistorique']
