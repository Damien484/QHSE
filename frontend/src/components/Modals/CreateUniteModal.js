import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { motion } from 'framer-motion';
import { createUnite } from '../../services/api';

function CreateUniteModal({ open, onClose, duerpId, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    nom: '',
    description: '',
    localisation: '',
    nombre_employes: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const dataToSend = {
        duerp_id: duerpId,
        ...formData,
        nombre_employes: formData.nombre_employes ? parseInt(formData.nombre_employes) : null,
      };

      await createUnite(dataToSend);
      setLoading(false);
      setFormData({ nom: '', description: '', localisation: '', nombre_employes: '' });
      onSuccess();
      onClose();
    } catch (err) {
      console.error('Erreur lors de la création de l\'unité:', err);
      setError(err.response?.data?.error || 'Une erreur est survenue');
      setLoading(false);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        component: motion.div,
        initial: { opacity: 0, scale: 0.9 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.9 },
        sx: {
          borderRadius: 3,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          backdropFilter: 'blur(10px)',
        },
      }}
    >
      <Box sx={{ background: 'white', borderRadius: 3 }}>
        <DialogTitle
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontWeight: 600,
          }}
        >
          Nouvelle Unité de Travail
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  label="Nom de l'unité"
                  name="nom"
                  value={formData.nom}
                  onChange={handleChange}
                  placeholder="Ex: Atelier de production"
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Décrivez l'unité de travail..."
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Localisation"
                  name="localisation"
                  value={formData.localisation}
                  onChange={handleChange}
                  placeholder="Ex: Bâtiment A - RDC"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Nombre d'employés"
                  name="nombre_employes"
                  value={formData.nombre_employes}
                  onChange={handleChange}
                  placeholder="Ex: 15"
                />
              </Grid>
            </Grid>
          </DialogContent>

          <DialogActions sx={{ p: 3 }}>
            <Button onClick={onClose} disabled={loading}>
              Annuler
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !formData.nom}
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
                },
              }}
            >
              {loading ? <CircularProgress size={24} /> : 'Créer l\'unité'}
            </Button>
          </DialogActions>
        </form>
      </Box>
    </Dialog>
  );
}

export default CreateUniteModal;
