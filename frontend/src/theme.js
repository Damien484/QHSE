import { createTheme } from '@mui/material/styles';

// Thème personnalisé pour l'application QHSE
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Bleu professionnel
      light: '#42a5f5',
      dark: '#1565c0',
      contrastText: '#fff',
    },
    secondary: {
      main: '#f50057', // Rose/Rouge pour les alertes
      light: '#ff4081',
      dark: '#c51162',
    },
    success: {
      main: '#4caf50', // Vert pour risques acceptables
      light: '#81c784',
      dark: '#388e3c',
    },
    warning: {
      main: '#ff9800', // Orange pour risques importants
      light: '#ffb74d',
      dark: '#f57c00',
    },
    error: {
      main: '#f44336', // Rouge pour risques critiques
      light: '#e57373',
      dark: '#d32f2f',
    },
    info: {
      main: '#2196f3',
      light: '#64b5f6',
      dark: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // Pas de majuscules automatiques
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

// Couleurs des niveaux de risque
export const riskColors = {
  Acceptable: '#4caf50',      // Vert
  'Modéré': '#ffeb3b',       // Jaune
  Important: '#ff9800',       // Orange
  Critique: '#f44336',        // Rouge
};

// Fonction pour obtenir la couleur d'un niveau de risque
export const getRiskColor = (niveau) => {
  return riskColors[niveau] || '#9e9e9e';
};

export default theme;
