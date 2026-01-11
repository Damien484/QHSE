import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Grid,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Add as AddIcon, Visibility as VisibilityIcon } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { getDUERPs } from '../services/api';

function DUERPList() {
  const [duerps, setDuerps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadDUERPs();
  }, []);

  const loadDUERPs = async () => {
    try {
      setLoading(true);
      const response = await getDUERPs();
      setDuerps(response.data.data || []);
      setLoading(false);
    } catch (err) {
      console.error('Erreur lors du chargement des DUERP:', err);
      setError('Impossible de charger la liste des DUERP');
      setLoading(false);
    }
  };

  const getStatusColor = (statut) => {
    switch (statut) {
      case 'validé':
        return 'success';
      case 'brouillon':
        return 'warning';
      case 'archivé':
        return 'default';
      default:
        return 'info';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" fontWeight={600}>
          Mes DUERP
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/duerp/nouveau')}
          size="large"
        >
          Nouveau DUERP
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {duerps.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Aucun DUERP créé
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Commencez par créer votre premier Document Unique d'Évaluation des Risques Professionnels
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/duerp/nouveau')}
              sx={{ mt: 2 }}
            >
              Créer mon premier DUERP
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {duerps.map((duerp, index) => (
            <Grid item xs={12} md={6} lg={4} key={duerp.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="start" mb={2}>
                      <Typography variant="h6" component="div">
                        {duerp.entreprise_nom}
                      </Typography>
                      <Chip
                        label={duerp.statut}
                        color={getStatusColor(duerp.statut)}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                      Version: {duerp.version}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                      Créé le: {new Date(duerp.date_creation).toLocaleDateString('fr-FR')}
                    </Typography>
                    {duerp.responsable_evaluation && (
                      <Typography variant="body2" color="textSecondary">
                        Responsable: {duerp.responsable_evaluation}
                      </Typography>
                    )}
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      startIcon={<VisibilityIcon />}
                      onClick={() => navigate(`/duerp/${duerp.id}`)}
                    >
                      Voir les détails
                    </Button>
                  </CardActions>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

export default DUERPList;
