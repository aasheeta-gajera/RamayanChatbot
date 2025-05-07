import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import AddIcon from '@mui/icons-material/Add';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Chatbot from './Chatbot';

// Create a Ramayan-themed color palette
const theme = createTheme({
  palette: {
    primary: {
      main: '#FF9933', // Saffron color
      light: '#FFB366',
      dark: '#CC7A29',
    },
    secondary: {
      main: '#800080', // Deep purple
      light: '#9932CC',
      dark: '#4B0082',
    },
    background: {
      default: '#FFFFFF',
      paper: '#FFF8DC',
    },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiIconButton: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: 'rgba(255, 153, 51, 0.1)',
          },
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: 'rgba(255, 153, 51, 0.1)',
          },
        },
      },
    },
  },
});

const drawerWidth = 280;

function AppContent() {
  const [open, setOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate('/');
  };

  const handleNewChat = () => {
    navigate('/chat');
    handleDrawerClose();
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar 
        position="fixed" 
        sx={{ 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: 'linear-gradient(45deg, #FF9933 30%, #FFB366 90%)',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ 
              mr: 2, 
              ...(open && { display: 'none' }),
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography 
            variant="h6" 
            noWrap 
            component="div" 
            sx={{ 
              flexGrow: 1,
              fontWeight: 600,
              textShadow: '1px 1px 2px rgba(0,0,0,0.2)',
            }}
          >
            Ramayan Chatbot
          </Typography>
          {!isAuthenticated ? (
            <>
              <IconButton 
                color="inherit" 
                onClick={() => setIsAuthenticated(true)}
                sx={{ 
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                <LoginIcon />
              </IconButton>
              <IconButton 
                color="inherit"
                sx={{ 
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                <PersonAddIcon />
              </IconButton>
            </>
          ) : (
            <IconButton 
              color="inherit" 
              onClick={handleLogout}
              sx={{ 
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              <LogoutIcon />
            </IconButton>
          
          )}
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: '#FFF8DC',
            borderRight: '2px solid #FF9933',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <Toolbar>
          <IconButton 
            onClick={handleDrawerClose}
            sx={{ 
              color: '#FF9933',
              '&:hover': {
                backgroundColor: 'rgba(255, 153, 51, 0.1)',
              },
            }}
          >
            <ChevronLeftIcon />
          </IconButton>
        </Toolbar>
        <Divider sx={{ borderColor: '#FF9933' }} />
        <List>
          <ListItem 
            button 
            onClick={handleNewChat}
            sx={{ 
              '&:hover': {
                backgroundColor: 'rgba(255, 153, 51, 0.1)',
              },
            }}
          >
            <ListItemIcon>
              <AddIcon sx={{ color: '#FF9933' }} />
            </ListItemIcon>
            <ListItemText 
              primary="New Chat" 
              primaryTypographyProps={{
                sx: { color: '#800080', fontWeight: 500 }
              }}
            />
          </ListItem>
        </List>
      </Drawer>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
          backgroundColor: '#FFFFFF',
        }}
      >
        <Routes>
          <Route path="/" element={
            <Box sx={{ 
              textAlign: 'center', 
              mt: 4,
              p: 4,
              backgroundColor: '#FFF8DC',
              borderRadius: 2,
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            }}>
              <Typography 
                variant="h4" 
                gutterBottom
                sx={{ 
                  color: '#800080',
                  fontWeight: 600,
                  mb: 3,
                }}
              >
                Welcome to Ramayan Chatbot
              </Typography>
              <Typography 
                variant="body1"
                sx={{ 
                  color: '#4B0082',
                  fontSize: '1.1rem',
                  lineHeight: 1.6,
                }}
              >
                Ask questions about the Ramayan and get instant answers
              </Typography>
            </Box>
          } />
          <Route path="/chat" element={<Chatbot />} />
        </Routes>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;
