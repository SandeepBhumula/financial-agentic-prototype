import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, PaletteMode } from '@mui/material/styles';
import { 
  CssBaseline, 
  Box, 
  Paper, 
  Container,
  useMediaQuery
} from '@mui/material';

import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import CardManagement from './pages/CardManagement';
import CardActivation from './pages/CardActivation';

// Create a theme instance with improved colors and typography
const theme = createTheme({
  palette: {
    primary: {
      light: '#4dabf5',
      main: '#1976d2',
      dark: '#1565c0',
      contrastText: '#fff',
    },
    secondary: {
      light: '#f73378',
      main: '#dc004e',
      dark: '#c51162',
      contrastText: '#fff',
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
    text: {
      primary: '#2a3548',
      secondary: '#546e7a',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
    h3: {
      fontWeight: 600,
    },
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
    h6: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            minHeight: '100vh',
            backgroundColor: theme.palette.background.default
          }}
        >
          <Navbar />
          <Container maxWidth="xl" sx={{ flexGrow: 1, py: 3, mt: 2 }}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 2, md: 3 }, 
                borderRadius: 3, 
                backgroundColor: 'transparent'
              }}
            >
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/cards" element={<CardManagement />} />
                <Route path="/activate" element={<CardActivation />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Paper>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
