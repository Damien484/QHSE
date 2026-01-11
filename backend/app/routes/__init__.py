"""
API Routes for QHSE application
"""
from flask import Blueprint

# Create blueprints
duerp_bp = Blueprint('duerp', __name__, url_prefix='/api/duerp')
unite_bp = Blueprint('unite', __name__, url_prefix='/api/unite')
risque_bp = Blueprint('risque', __name__, url_prefix='/api/risque')
mesure_bp = Blueprint('mesure', __name__, url_prefix='/api/mesure')

# Import routes to register them
from . import duerp_routes, unite_routes, risque_routes, mesure_routes

__all__ = ['duerp_bp', 'unite_bp', 'risque_bp', 'mesure_bp']
