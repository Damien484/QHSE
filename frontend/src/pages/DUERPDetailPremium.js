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
  IconButton,
  Fab,
  Tooltip,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Download as DownloadIcon,
  Assessment as AssessmentIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { getDUERP, getDUERPStats, generateDUERPDocument, deleteUnite } from '../services/api';
import { getRiskColor } from '../theme';
import CreateUniteModal from '../components/Modals/CreateUniteModal';

// Animations sophistiquées
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      type: 'spring',
      stiffness: 100,
    },
  },
};

const cardVariants = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      type: 'spring',
      stiffness: 200,
      damping: 20,
    },
  },
  hover: {
    scale: 1.05,
    boxShadow: '0 20px 40px rgba(0,0,0,0.2)',
    transition: {
      type: 'spring',
      stiffness: 400,
      damping: 10,
    },
  },
};

function DUERPDetailPremium() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [duerp, setDuerp] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const [createUniteOpen, setCreateUniteOpen] = useState(false);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    await loadDUERP();
    await loadStats();
  };

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

  const handleDeleteUnite = async (uniteId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette unité ?')) {
      try {
        await deleteUnite(uniteId);
        await loadData();
      } catch (err) {
        console.error('Erreur lors de la suppression:', err);
        setError('Impossible de supprimer l\'unité');
      }
    }
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="60vh"
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: 4,
        }}
      >
        <CircularProgress size={60} sx={{ color: 'white' }} />
      </Box>
    );
  }

  if (error || !duerp) {
    return (
      <Alert severity="error" sx={{ borderRadius: 3 }}>
        {error || 'DUERP introuvable'}
      </Alert>
    );
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header avec effet glassmorphism */}
      <motion.div variants={itemVariants}>
        <Paper
          elevation={0}
          sx={{
            p: 3,
            mb: 3,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 4,
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'rgba(255,255,255,0.1)',
              backdropFilter: 'blur(10px)',
            },
          }}
        >
          <Box display="flex" alignItems="center" position="relative" zIndex={1}>
            <IconButton
              onClick={() => navigate('/duerp')}
              sx={{ color: 'white', mr: 2 }}
            >
              <ArrowBackIcon />
            </IconButton>
            <Box flexGrow={1}>
              <Typography variant="h4" fontWeight={700}>
                {duerp.entreprise_nom}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9, mt: 1 }}>
                Version {duerp.version} • {duerp.statut}
              </Typography>
            </Box>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                variant="contained"
                startIcon={downloading ? <CircularProgress size={20} /> : <DownloadIcon />}
                onClick={handleDownloadPDF}
                disabled={downloading}
                sx={{
                  backgroundColor: 'white',
                  color: '#667eea',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.9)',
                  },
                  borderRadius: 2,
                  px: 3,
                }}
              >
                {downloading ? 'Génération...' : 'Télécharger PDF'}
              </Button>
            </motion.div>
          </Box>
        </Paper>
      </motion.div>

      <Grid container spacing={3}>
        {/* Carte statistiques premium */}
        <Grid item xs={12} md={4}>
          <motion.div variants={cardVariants} whileHover="hover">
            <Card
              sx={{
                borderRadius: 4,
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                color: 'white',
                height: '100%',
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <AssessmentIcon sx={{ fontSize: 40, mr: 1 }} />
                  <Typography variant="h5" fontWeight={700}>
                    Statistiques
                  </Typography>
                </Box>
                <Divider sx={{ borderColor: 'rgba(255,255,255,0.3)', mb: 2 }} />
                {stats && (
                  <>
                    <Box mb={2}>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        Unités de travail
                      </Typography>
                      <Typography variant="h3" fontWeight={700}>
                        {stats.nombre_unites || 0}
                      </Typography>
                    </Box>
                    <Box mb={2}>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        Total risques
                      </Typography>
                      <Typography variant="h3" fontWeight={700}>
                        {stats.nombre_risques_total || 0}
                      </Typography>
                    </Box>
                    {stats.nombre_risques_par_niveau &&
                      Object.entries(stats.nombre_risques_par_niveau).map(([niveau, nombre]) => (
                        <Box
                          key={niveau}
                          display="flex"
                          justifyContent="space-between"
                          alignItems="center"
                          mt={1}
                          p={1}
                          sx={{
                            background: 'rgba(255,255,255,0.2)',
                            borderRadius: 2,
                          }}
                        >
                          <Typography variant="body2">{niveau}</Typography>
                          <Typography variant="h6" fontWeight={700}>
                            {nombre}
                          </Typography>
                        </Box>
                      ))}
                  </>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Informations principales */}
        <Grid item xs={12} md={8}>
          <motion.div variants={cardVariants} whileHover="hover">
            <Paper
              elevation={0}
              sx={{
                p: 3,
                borderRadius: 4,
                background: 'white',
                border: '1px solid',
                borderColor: 'divider',
              }}
            >
              <Typography variant="h6" gutterBottom fontWeight={700} color="primary">
                Informations générales
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    SIRET
                  </Typography>
                  <Typography variant="body1" fontWeight={500}>
                    {duerp.entreprise_siret || 'Non renseigné'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Effectif
                  </Typography>
                  <Typography variant="body1" fontWeight={500}>
                    {duerp.effectif || 'Non renseigné'}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    Adresse
                  </Typography>
                  <Typography variant="body1" fontWeight={500}>
                    {duerp.entreprise_adresse || 'Non renseignée'}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    Activité
                  </Typography>
                  <Typography variant="body1" fontWeight={500}>
                    {duerp.entreprise_activite || 'Non renseignée'}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </motion.div>
        </Grid>

        {/* Unités de travail */}
        <Grid item xs={12}>
          <motion.div variants={itemVariants}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                borderRadius: 4,
                background: 'white',
                border: '1px solid',
                borderColor: 'divider',
              }}
            >
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" fontWeight={700} color="primary">
                  Unités de travail
                </Typography>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setCreateUniteOpen(true)}
                    sx={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      borderRadius: 2,
                    }}
                  >
                    Ajouter une unité
                  </Button>
                </motion.div>
              </Box>
              <Divider sx={{ mb: 2 }} />

              {duerp.unites_travail && duerp.unites_travail.length > 0 ? (
                <Grid container spacing={2}>
                  <AnimatePresence>
                    {duerp.unites_travail.map((unite, index) => (
                      <Grid item xs={12} md={6} key={unite.id}>
                        <motion.div
                          variants={cardVariants}
                          initial="hidden"
                          animate="visible"
                          exit="hidden"
                          custom={index}
                          whileHover="hover"
                        >
                          <Card
                            variant="outlined"
                            sx={{
                              borderRadius: 3,
                              borderWidth: 2,
                              borderColor: 'primary.main',
                              position: 'relative',
                              overflow: 'visible',
                            }}
                          >
                            <CardContent>
                              <Box display="flex" justifyContent="space-between" alignItems="start">
                                <Typography variant="h6" fontWeight={700} color="primary">
                                  {unite.nom}
                                </Typography>
                                <IconButton
                                  size="small"
                                  onClick={() => handleDeleteUnite(unite.id)}
                                  sx={{ color: 'error.main' }}
                                >
                                  <DeleteIcon fontSize="small" />
                                </IconButton>
                              </Box>
                              <Typography variant="body2" color="textSecondary" paragraph>
                                {unite.description}
                              </Typography>
                              <Box display="flex" gap={1} flexWrap="wrap">
                                <Chip
                                  label={`${unite.risques?.length || 0} risques`}
                                  size="small"
                                  color="warning"
                                  icon={<WarningIcon />}
                                />
                                {unite.localisation && (
                                  <Chip label={unite.localisation} size="small" variant="outlined" />
                                )}
                              </Box>
                            </CardContent>
                          </Card>
                        </motion.div>
                      </Grid>
                    ))}
                  </AnimatePresence>
                </Grid>
              ) : (
                <Alert
                  severity="info"
                  sx={{ borderRadius: 2 }}
                  action={
                    <Button
                      color="inherit"
                      size="small"
                      onClick={() => setCreateUniteOpen(true)}
                    >
                      Créer
                    </Button>
                  }
                >
                  Aucune unité de travail définie. Ajoutez des unités pour commencer l'évaluation
                  des risques.
                </Alert>
              )}
            </Paper>
          </motion.div>
        </Grid>
      </Grid>

      {/* Modal création unité */}
      <CreateUniteModal
        open={createUniteOpen}
        onClose={() => setCreateUniteOpen(false)}
        duerpId={id}
        onSuccess={loadData}
      />

      {/* FAB flottant */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.5, type: 'spring' }}
      >
        <Tooltip title="Ajouter une unité" placement="left">
          <Fab
            color="primary"
            sx={{
              position: 'fixed',
              bottom: 24,
              right: 24,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            }}
            onClick={() => setCreateUniteOpen(true)}
          >
            <AddIcon />
          </Fab>
        </Tooltip>
      </motion.div>
    </motion.div>
  );
}

export default DUERPDetailPremium;
