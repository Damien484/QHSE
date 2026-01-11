import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Paper,
  Grid,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  Card,
  CardContent,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Download as DownloadIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { getDUERP, getDUERPStats, generateDUERPDocument } from '../services/api';
import { getRiskColor } from '../theme';

function DUERPDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [duerp, setDuerp] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    loadDUERP();
    loadStats();
  }, [id]);

  const loadDUERP = async () => {
    try {
      setLoading(true);
      const response = await getDUERP(id);
      setDuerp(response.data.data);
      setLoading(false);
    } catch (err) {
      console.error('Erreur lors du chargement du DUERP:', err);
      setError('Impossible de charger les détails du DUERP');
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await getDUERPStats(id);
      setStats(response.data.data);
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      setDownloading(true);
      const response = await generateDUERPDocument(id, 'pdf');

      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `DUERP_${duerp.entreprise_nom}_${duerp.version}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      setDownloading(false);
    } catch (err) {
      console.error('Erreur lors du téléchargement:', err);
      setError('Impossible de générer le document PDF');
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error || !duerp) {
    return (
      <Alert severity="error">{error || 'DUERP introuvable'}</Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" mb={4}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/duerp')}
          sx={{ mr: 2 }}
        >
          Retour
        </Button>
        <Box flexGrow={1}>
          <Typography variant="h4" fontWeight={600}>
            {duerp.entreprise_nom}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<DownloadIcon />}
          onClick={handleDownloadPDF}
          disabled={downloading}
        >
          {downloading ? 'Génération...' : 'Télécharger PDF'}
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Informations principales */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Informations générales
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">Version</Typography>
                <Typography variant="body1">{duerp.version}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">Statut</Typography>
                <Chip label={duerp.statut} color={duerp.statut === 'validé' ? 'success' : 'warning'} size="small" />
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">SIRET</Typography>
                <Typography variant="body1">{duerp.entreprise_siret || 'Non renseigné'}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">Effectif</Typography>
                <Typography variant="body1">{duerp.effectif || 'Non renseigné'}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">Adresse</Typography>
                <Typography variant="body1">{duerp.entreprise_adresse || 'Non renseignée'}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">Activité</Typography>
                <Typography variant="body1">{duerp.entreprise_activite || 'Non renseignée'}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">Responsable évaluation</Typography>
                <Typography variant="body1">{duerp.responsable_evaluation || 'Non renseigné'}</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Statistiques */}
        <Grid item xs={12} md={4}>
          {stats && (
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <AssessmentIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Statistiques</Typography>
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Box mb={2}>
                  <Typography variant="body2" color="textSecondary">Unités de travail</Typography>
                  <Typography variant="h4">{stats.nombre_unites || 0}</Typography>
                </Box>
                <Box mb={2}>
                  <Typography variant="body2" color="textSecondary">Total risques</Typography>
                  <Typography variant="h4">{stats.nombre_risques_total || 0}</Typography>
                </Box>
                <Box mb={2}>
                  <Typography variant="body2" color="textSecondary">Risques par niveau</Typography>
                  {stats.nombre_risques_par_niveau && Object.entries(stats.nombre_risques_par_niveau).map(([niveau, nombre]) => (
                    <Box key={niveau} display="flex" justifyContent="space-between" alignItems="center" mt={1}>
                      <Chip
                        label={niveau}
                        size="small"
                        sx={{ backgroundColor: getRiskColor(niveau), color: '#fff' }}
                      />
                      <Typography variant="body2">{nombre}</Typography>
                    </Box>
                  ))}
                </Box>
                <Box>
                  <Typography variant="body2" color="textSecondary">Mesures de prévention</Typography>
                  <Typography variant="h4">{stats.nombre_mesures_prevention || 0}</Typography>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>

        {/* Liste des unités de travail */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Unités de travail
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {duerp.unites_travail && duerp.unites_travail.length > 0 ? (
              <Grid container spacing={2}>
                {duerp.unites_travail.map((unite) => (
                  <Grid item xs={12} md={6} key={unite.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6">{unite.nom}</Typography>
                        <Typography variant="body2" color="textSecondary" paragraph>
                          {unite.description}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Risques identifiés: {unite.risques?.length || 0}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Alert severity="info">
                Aucune unité de travail définie. Ajoutez des unités de travail pour commencer l'évaluation des risques.
              </Alert>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default DUERPDetail;
