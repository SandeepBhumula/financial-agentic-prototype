import React, { useState } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box, 
  Container, 
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Badge,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import NotificationsIcon from '@mui/icons-material/Notifications';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import AddCardIcon from '@mui/icons-material/AddCard';
import LogoutIcon from '@mui/icons-material/Logout';
import CloseIcon from '@mui/icons-material/Close';

const Navbar: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();
  
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  
  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleMenuClose = () => {
    setAnchorEl(null);
  };
  
  const toggleDrawer = () => {
    setMobileOpen(!mobileOpen);
  };
  
  const menuItems = [
    { text: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { text: 'My Cards', path: '/cards', icon: <CreditCardIcon /> },
    { text: 'Activate Card', path: '/activate', icon: <AddCardIcon /> },
  ];
  
  const isActive = (path: string) => location.pathname === path;
  
  const drawer = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between', 
        p: 2, 
        bgcolor: 'primary.main',
        color: 'white'
      }}>
        <Typography variant="h6">Menu</Typography>
        <IconButton color="inherit" onClick={toggleDrawer}>
          <CloseIcon />
        </IconButton>
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem 
            button 
            key={item.text} 
            component={RouterLink} 
            to={item.path}
            onClick={toggleDrawer}
            sx={{
              bgcolor: isActive(item.path) ? 'rgba(25, 118, 210, 0.1)' : 'transparent',
              color: isActive(item.path) ? 'primary.main' : 'inherit',
              '&:hover': {
                bgcolor: 'rgba(25, 118, 210, 0.05)',
              },
            }}
          >
            <ListItemIcon sx={{ color: isActive(item.path) ? 'primary.main' : 'inherit' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        <ListItem button>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </Box>
  );
  
  return (
    <>
      <AppBar 
        position="sticky" 
        elevation={0}
        sx={{ 
          bgcolor: 'white', 
          color: 'text.primary',
          borderBottom: 1,
          borderColor: 'divider'
        }}
      >
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            {isMobile && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={toggleDrawer}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
            )}
            
            <Typography
              variant="h6"
              noWrap
              component={RouterLink}
              to="/"
              sx={{ 
                mr: 2, 
                display: 'flex', 
                fontWeight: 700,
                letterSpacing: '.05rem',
                color: 'primary.main',
                textDecoration: 'none',
                flexGrow: isMobile ? 1 : 0
              }}
            >
              Financial Services
            </Typography>

            {!isMobile && (
              <Box sx={{ flexGrow: 1, display: 'flex', ml: 4 }}>
                {menuItems.map((item) => (
                  <Button
                    key={item.text}
                    component={RouterLink}
                    to={item.path}
                    startIcon={item.icon}
                    sx={{ 
                      mr: 2, 
                      color: isActive(item.path) ? 'primary.main' : 'text.primary',
                      bgcolor: isActive(item.path) ? 'rgba(25, 118, 210, 0.1)' : 'transparent',
                      '&:hover': {
                        bgcolor: 'rgba(25, 118, 210, 0.05)',
                      },
                      fontWeight: isActive(item.path) ? 600 : 500,
                    }}
                  >
                    {item.text}
                  </Button>
                ))}
              </Box>
            )}

            <Box sx={{ flexGrow: 0, display: 'flex', alignItems: 'center' }}>
              <IconButton color="inherit" sx={{ ml: 1 }}>
                <Badge badgeContent={3} color="error">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
              
              <IconButton 
                edge="end" 
                color="inherit" 
                sx={{ ml: 2 }}
                onClick={handleProfileMenuOpen}
              >
                <Avatar 
                  sx={{ 
                    width: 32, 
                    height: 32,
                    bgcolor: 'primary.main'
                  }}
                >
                  <AccountCircleIcon />
                </Avatar>
              </IconButton>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      
      {/* Mobile Drawer */}
      <Drawer
        anchor="left"
        open={isMobile && mobileOpen}
        onClose={toggleDrawer}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile
        }}
      >
        {drawer}
      </Drawer>
      
      {/* User Profile Menu */}
      <Menu
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
        <MenuItem onClick={handleMenuClose}>My Account</MenuItem>
        <Divider />
        <MenuItem onClick={handleMenuClose}>Logout</MenuItem>
      </Menu>
    </>
  );
};

export default Navbar; 