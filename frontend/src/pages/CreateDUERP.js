import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Alert,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { Save as SaveIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { createDUERP } from '../services/api';

const steps = ['Informations entreprise', 'Responsables', 'Finalisation'];

function CreateDUERP() {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    entreprise_nom: '',
    entreprise_siret: '',
    entreprise_adresse: '',
    entreprise_activite: '',
    effectif: '',
    responsable_evaluation: '',
    responsable_validation: '',
    version: '1.0',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleNext = () => {
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const dataToSend = {
        ...formData,
        effectif: formData.effectif ? parseInt(formData.effectif) : null,
      };

      const response = await createDUERP(dataToSend);
      setSuccess(true);
      setLoading(false);

      // Rediriger vers le DUERP créé après 2 secondes
      setTimeout(() => {
        navigate(`/duerp/${response.data.data.id}`);
      }, 2000);
    } catch (err) {
      console.error('Erreur lors de la création du DUERP:', err);
      setError(err.response?.data?.error || 'Une erreur est survenue lors de la création du DUERP');
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Nom de l'entreprise"
                name="entreprise_nom"
                value={formData.entreprise_nom}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="SIRET"
                name="entreprise_siret"
                value={formData.entreprise_siret}
                onChange={handleChange}
                inputProps={{ maxLength: 14 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Effectif"
                name="effectif"
                value={formData.effectif}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Adresse"
                name="entreprise_adresse"
                value={formData.entreprise_adresse}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Activité principale"
                name="entreprise_activite"
                value={formData.entreprise_activite}
                onChange={handleChange}
              />
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Responsable de l'évaluation"
                name="responsable_evaluation"
                value={formData.responsable_evaluation}
                onChange={handleChange}
                helperText="Personne en charge de l'évaluation des risques"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Responsable de la validation"
                name="responsable_validation"
                value={formData.responsable_validation}
                onChange={handleChange}
                helperText="Personne qui valide le document (généralement le dirigeant)"
              />
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Récapitulatif
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  Entreprise: <strong>{formData.entreprise_nom || 'Non renseigné'}</strong>
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  SIRET: <strong>{formData.entreprise_siret || 'Non renseigné'}</strong>
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  Effectif: <strong>{formData.effectif || 'Non renseigné'}</strong>
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  Responsable évaluation: <strong>{formData.responsable_evaluation || 'Non renseigné'}</strong>
                </Typography>
              </Grid>
            </Grid>
          </Box>
        );
      default:
        return null;
    }
  };

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
        <Typography variant="h4" fontWeight={600}>
          Nouveau DUERP
        </Typography>
      </Box>

      <Paper sx={{ p: 4 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            DUERP créé avec succès ! Redirection...
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          {renderStepContent(activeStep)}

          <Box display="flex" justifyContent="space-between" mt={4}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Précédent
            </Button>
            <Box>
              {activeStep < steps.length - 1 ? (
                <Button
                  variant="contained"
                  onClick={handleNext}
                  disabled={!formData.entreprise_nom}
                >
                  Suivant
                </Button>
              ) : (
                <Button
                  variant="contained"
                  type="submit"
                  startIcon={<SaveIcon />}
                  disabled={loading || !formData.entreprise_nom}
                >
                  {loading ? 'Création...' : 'Créer le DUERP'}
                </Button>
              )}
            </Box>
          </Box>
        </form>
      </Paper>
    </Box>
  );
}

export default CreateDUERP;
