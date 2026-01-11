import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';

// Layout
import Layout from './components/Layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import DUERPList from './pages/DUERPList';
import DUERPDetailPremium from './pages/DUERPDetailPremium';
import CreateDUERP from './pages/CreateDUERP';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/duerp" element={<DUERPList />} />
            <Route path="/duerp/nouveau" element={<CreateDUERP />} />
            <Route path="/duerp/:id" element={<DUERPDetailPremium />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
