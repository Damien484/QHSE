import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Description as DescriptionIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { getDUERPs } from '../services/api';

// Composant pour les cartes de statistiques
const StatCard = ({ title, value, icon, color, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
  >
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h3" component="div" color={color}>
              {value}
            </Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: `${color}.lighter`,
              borderRadius: '50%',
              p: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {React.cloneElement(icon, { sx: { fontSize: 40, color } })}
          </Box>
        </Box>
      </CardContent>
    </Card>
  </motion.div>
);

function Dashboard() {
  const [stats, setStats] = useState({
    totalDUERP: 0,
    duerpsActifs: 0,
    risquesCritiques: 0,
    tauxConformite: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await getDUERPs();
      const duerps = response.data.data || [];

      // Calculer les statistiques
      const totalDUERP = duerps.length;
      const duerpsActifs = duerps.filter(d => d.statut === 'validé').length;

      setStats({
        totalDUERP,
        duerpsActifs,
        risquesCritiques: 0, // À calculer depuis l'API
        tauxConformite: totalDUERP > 0 ? Math.round((duerpsActifs / totalDUERP) * 100) : 0,
      });

      setLoading(false);
    } catch (err) {
      console.error('Erreur lors du chargement du dashboard:', err);
      setError('Impossible de charger les données du tableau de bord');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
          Tableau de bord
        </Typography>
      </motion.div>

      <Grid container spacing={3}>
        {/* Carte Total DUERP */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total DUERP"
            value={stats.totalDUERP}
            icon={<DescriptionIcon />}
            color="primary.main"
            delay={0.1}
          />
        </Grid>

        {/* Carte DUERP Actifs */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="DUERP Validés"
            value={stats.duerpsActifs}
            icon={<CheckCircleIcon />}
            color="success.main"
            delay={0.2}
          />
        </Grid>

        {/* Carte Risques Critiques */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Risques Critiques"
            value={stats.risquesCritiques}
            icon={<WarningIcon />}
            color="error.main"
            delay={0.3}
          />
        </Grid>

        {/* Carte Taux de Conformité */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Taux de Conformité"
            value={`${stats.tauxConformite}%`}
            icon={<TrendingUpIcon />}
            color="info.main"
            delay={0.4}
          />
        </Grid>

        {/* Carte de bienvenue */}
        <Grid item xs={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Bienvenue dans l'application QHSE
                </Typography>
                <Typography variant="body1" color="textSecondary">
                  Cette application vous permet de gérer vos Documents Uniques d'Évaluation des Risques
                  Professionnels (DUERP) de manière simple et conforme à la réglementation française.
                </Typography>
                <Box mt={2}>
                  <Typography variant="body2" color="textSecondary">
                    • Créez et gérez vos DUERP
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    • Évaluez les risques professionnels avec calcul automatique de criticité
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    • Planifiez les mesures de prévention
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    • Générez des documents PDF professionnels
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
