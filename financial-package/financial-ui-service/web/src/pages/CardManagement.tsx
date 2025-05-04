import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Divider,
  Chip,
  Paper,
  Tabs,
  Tab,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  useTheme,
  useMediaQuery,
  CardHeader,
  Stack,
  LinearProgress,
  Tooltip,
  Alert
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import LockIcon from '@mui/icons-material/Lock';
import SecurityIcon from '@mui/icons-material/Security';
import WarningIcon from '@mui/icons-material/Warning';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import ReceiptIcon from '@mui/icons-material/Receipt';
import CircleIcon from '@mui/icons-material/Circle';
import { Link as RouterLink } from 'react-router-dom';

// Mock card data
const cards = [
  {
    id: 1,
    name: 'Cash Rewards Credit Card',
    type: 'Credit',
    lastFour: '1234',
    expiryDate: '05/25',
    availableCredit: 7500,
    usedCredit: 2500,
    status: 'Active',
    isVirtual: false,
    cardHolder: 'John Smith',
    rewards: 325,
    limit: 10000,
    transactions: [
      { id: 1, merchant: 'Amazon', amount: 43.65, date: '2023-06-14', category: 'Shopping' },
      { id: 2, merchant: 'Starbucks', amount: 5.45, date: '2023-06-13', category: 'Dining' },
      { id: 3, merchant: 'Uber', amount: 24.50, date: '2023-06-11', category: 'Transport' }
    ]
  },
  {
    id: 2,
    name: 'Premium Travel Card',
    type: 'Credit',
    lastFour: '5678',
    expiryDate: '09/26',
    availableCredit: 15000,
    usedCredit: 4200,
    status: 'Active',
    isVirtual: false,
    cardHolder: 'John Smith',
    rewards: 1240,
    limit: 20000,
    transactions: [
      { id: 1, merchant: 'United Airlines', amount: 543.65, date: '2023-06-01', category: 'Travel' },
      { id: 2, merchant: 'Hilton Hotels', amount: 275.45, date: '2023-05-28', category: 'Travel' },
      { id: 3, merchant: 'Restaurant XYZ', amount: 124.50, date: '2023-05-27', category: 'Dining' }
    ]
  },
  {
    id: 3,
    name: 'Health Savings Debit',
    type: 'Debit',
    lastFour: '9012',
    expiryDate: '12/24',
    balance: 2340.75,
    status: 'Pending Activation',
    isVirtual: true,
    cardHolder: 'John Smith',
    transactions: []
  },
  {
    id: 4,
    name: 'Business Expense Card',
    type: 'Credit',
    lastFour: '3456',
    expiryDate: '08/25',
    availableCredit: 25000,
    usedCredit: 12000,
    status: 'Temporarily Locked',
    isVirtual: false,
    cardHolder: 'Smith Business LLC',
    rewards: 780,
    limit: 30000,
    transactions: [
      { id: 1, merchant: 'Office Supplies Inc', amount: 143.65, date: '2023-06-10', category: 'Business' },
      { id: 2, merchant: 'Adobe', amount: 52.99, date: '2023-06-05', category: 'Software' },
      { id: 3, merchant: 'Business Lunch', amount: 84.50, date: '2023-06-02', category: 'Dining' }
    ]
  }
];

// Card color mapping with enhanced gradients
const cardColors: {[key: string]: {background: string, text: string}} = {
  'Credit': {
    background: 'linear-gradient(135deg, #1976d2 0%, #0d47a1 100%)',
    text: '#ffffff'
  },
  'Debit': {
    background: 'linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)',
    text: '#ffffff'
  },
  'Prepaid': {
    background: 'linear-gradient(135deg, #f57c00 0%, #e65100 100%)',
    text: '#ffffff'
  }
};

// Status color mapping
const statusColors: {[key: string]: {color: string}} = {
  'Active': { color: 'success.main' },
  'Temporarily Locked': { color: 'warning.main' },
  'Pending Activation': { color: 'info.main' },
  'Inactive': { color: 'text.disabled' }
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`card-tabpanel-${index}`}
      aria-labelledby={`card-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: { xs: 2, md: 3 } }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const StyledCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  height: 200,
  borderRadius: theme.shape.borderRadius,
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: '0 12px 20px rgba(0,0,0,0.2)'
  }
}));

// Enhanced credit card component with chip and logo
const CreditCardDisplay = styled(Box)(({ theme }) => ({
  width: '100%',
  height: '100%',
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
}));

const CardChip = styled(Box)(({ theme }) => ({
  width: 40,
  height: 30,
  backgroundColor: 'rgba(255, 255, 255, 0.5)',
  borderRadius: 5,
  marginBottom: theme.spacing(1),
  position: 'relative',
  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent 50%, rgba(255, 255, 255, 0.3) 70%, transparent 90%)',
    borderRadius: 5,
  }
}));

const CardManagement: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [tabValue, setTabValue] = useState(0);
  const [activeCardId, setActiveCardId] = useState<number | null>(null);
  const [showFullCardNumber, setShowFullCardNumber] = useState<{[key: number]: boolean}>({});
  const [lockCardDialogOpen, setLockCardDialogOpen] = useState(false);
  const [selectedCard, setSelectedCard] = useState<number | null>(null);
  const [reportLostDialogOpen, setReportLostDialogOpen] = useState(false);
  const [requestLimitDialogOpen, setRequestLimitDialogOpen] = useState(false);
  const [newCardDialogOpen, setNewCardDialogOpen] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };
  
  const handleCardClick = (cardId: number) => {
    setActiveCardId(activeCardId === cardId ? null : cardId);
  };

  const toggleCardVisibility = (cardId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setShowFullCardNumber(prev => ({ 
      ...prev, 
      [cardId]: !prev[cardId] 
    }));
  };

  const handleLockCard = (cardId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setSelectedCard(cardId);
    setLockCardDialogOpen(true);
  };

  const handleReportLost = (cardId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setSelectedCard(cardId);
    setReportLostDialogOpen(true);
  };

  const handleRequestLimit = (cardId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setSelectedCard(cardId);
    setRequestLimitDialogOpen(true);
  };
  
  const handleNewCard = () => {
    setNewCardDialogOpen(true);
  };

  const closeLockCardDialog = () => {
    setLockCardDialogOpen(false);
    setSelectedCard(null);
  };

  const closeReportLostDialog = () => {
    setReportLostDialogOpen(false);
    setSelectedCard(null);
  };

  const closeRequestLimitDialog = () => {
    setRequestLimitDialogOpen(false);
    setSelectedCard(null);
  };
  
  const closeNewCardDialog = () => {
    setNewCardDialogOpen(false);
  };

  // Filter cards based on tab
  const getFilteredCards = () => {
    if (tabValue === 0) return cards; // All cards
    if (tabValue === 1) return cards.filter(card => card.type === 'Credit');
    if (tabValue === 2) return cards.filter(card => card.type === 'Debit');
    if (tabValue === 3) return cards.filter(card => card.status === 'Pending Activation');
    return [];
  };

  const calculateUtilization = (used: number, limit: number) => {
    return Math.round((used / limit) * 100);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" fontWeight="bold" color="primary.dark">
          Card Management
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddCircleOutlineIcon />}
          onClick={handleNewCard}
          sx={{ borderRadius: 8 }}
        >
          Request New Card
        </Button>
      </Box>
      
      <Paper sx={{ width: '100%', mb: 4, borderRadius: 3, overflow: 'hidden' }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange}
          variant={isMobile ? "scrollable" : "fullWidth"}
          scrollButtons={isMobile ? "auto" : undefined}
          indicatorColor="primary"
          textColor="primary"
          sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'grey.50' }}
        >
          <Tab label="All Cards" icon={<CreditCardIcon />} iconPosition="start" />
          <Tab label="Credit Cards" icon={<AttachMoneyIcon />} iconPosition="start" />
          <Tab label="Debit Cards" icon={<AccountBalanceWalletIcon />} iconPosition="start" />
          <Tab label="Pending Activation" icon={<ReceiptIcon />} iconPosition="start" />
        </Tabs>
        
        <TabPanel value={tabValue} index={tabValue}>
          <Grid container spacing={3}>
            {getFilteredCards().map(card => (
              <Grid item key={card.id} xs={12} md={6} lg={4}>
                <Box onClick={() => handleCardClick(card.id)}>
                  <StyledCard 
                    elevation={4}
                    sx={{
                      background: cardColors[card.type].background,
                      color: cardColors[card.type].text,
                      opacity: card.status === 'Temporarily Locked' ? 0.8 : 1,
                      cursor: 'pointer',
                      mb: 2
                    }}
                  >
                    <CreditCardDisplay>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                        <Box>
                          <Typography variant="h6" fontWeight="500">{card.name}</Typography>
                          <Box display="flex" alignItems="center" mt={1}>
                            <CardChip />
                            {card.isVirtual && (
                              <Chip 
                                size="small" 
                                label="Virtual" 
                                sx={{ ml: 1, bgcolor: 'rgba(255,255,255,0.2)', color: 'inherit' }} 
                              />
                            )}
                          </Box>
                        </Box>
                        <Box>
                          <Typography variant="caption" component="div" sx={{ textAlign: 'right', opacity: 0.8 }}>
                            {card.type.toUpperCase()}
                          </Typography>
                          <Chip 
                            size="small"
                            icon={<CircleIcon sx={{ fontSize: '0.6rem !important' }} />}
                            label={card.status}
                            sx={{ 
                              mt: 0.5,
                              bgcolor: 'rgba(255,255,255,0.2)', 
                              color: 'inherit',
                              '& .MuiChip-icon': { color: statusColors[card.status].color }
                            }} 
                          />
                        </Box>
                      </Box>

                      <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
                        <Typography variant="body1" letterSpacing={1}>
                          {showFullCardNumber[card.id] ? 
                            "4012 8888 8888 " + card.lastFour : 
                            "•••• •••• •••• " + card.lastFour
                          }
                        </Typography>
                        <IconButton 
                          size="small" 
                          onClick={(e) => toggleCardVisibility(card.id, e)}
                          sx={{ ml: 1, color: 'inherit', opacity: 0.8 }}
                        >
                          {showFullCardNumber[card.id] ? <VisibilityOffIcon /> : <VisibilityIcon />}
                        </IconButton>
                      </Box>

                      <Box display="flex" justifyContent="space-between" alignItems="flex-end">
                        <Typography variant="body2">
                          {card.cardHolder}
                        </Typography>
                        <Typography variant="body2">
                          Exp: {card.expiryDate}
                        </Typography>
                      </Box>

                      {card.status === 'Temporarily Locked' && (
                        <Box sx={{ 
                          position: 'absolute', 
                          top: 0, 
                          left: 0, 
                          right: 0, 
                          bottom: 0, 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center',
                          bgcolor: 'rgba(0,0,0,0.4)',
                          borderRadius: 'inherit'
                        }}>
                          <LockIcon sx={{ fontSize: 64, opacity: 0.8 }} />
                        </Box>
                      )}
                    </CreditCardDisplay>
                  </StyledCard>
                  
                  <Paper 
                    elevation={2} 
                    sx={{ 
                      p: 0, 
                      borderRadius: 3, 
                      transition: 'all 0.3s',
                      maxHeight: activeCardId === card.id ? '1000px' : '160px',
                      overflow: 'hidden'
                    }}
                  >
                    <CardHeader
                      title={
                        <Typography variant="subtitle1">
                          {card.type === 'Credit' ? 'Card Details' : 'Account Details'}
                        </Typography>
                      }
                      action={
                        card.status === 'Pending Activation' ? (
                          <Button 
                            size="small" 
                            color="primary" 
                            variant="contained"
                            component={RouterLink} 
                            to="/activate"
                          >
                            Activate Now
                          </Button>
                        ) : (
                          <Button 
                            size="small" 
                            variant="outlined"
                            color={card.status === 'Temporarily Locked' ? "success" : "warning"}
                            startIcon={<LockIcon />}
                            onClick={(e) => handleLockCard(card.id, e)}
                          >
                            {card.status === 'Temporarily Locked' ? 'Unlock' : 'Lock'}
                          </Button>
                        )
                      }
                      sx={{ p: 2, bgcolor: 'grey.50' }}
                    />
                    <Divider />
                    <CardContent sx={{ pt: 2 }}>
                      {card.type === 'Credit' && (
                        <>
                          <Stack spacing={1}>
                            <Box>
                              <Box display="flex" justifyContent="space-between" alignItems="center">
                                <Typography variant="body2" color="text.secondary">Available Credit:</Typography>
                                <Typography variant="body2" fontWeight="500">${card.availableCredit?.toLocaleString()}</Typography>
                              </Box>
                              <Box display="flex" alignItems="center" mt={0.5}>
                                <LinearProgress
                                  variant="determinate"
                                  value={calculateUtilization(card.usedCredit, card.limit)}
                                  sx={{ 
                                    width: '100%', 
                                    height: 8, 
                                    borderRadius: 4,
                                    bgcolor: 'grey.200',
                                    '& .MuiLinearProgress-bar': {
                                      bgcolor: calculateUtilization(card.usedCredit, card.limit) > 80 
                                        ? 'error.main' 
                                        : calculateUtilization(card.usedCredit, card.limit) > 50 
                                          ? 'warning.main' 
                                          : 'success.main',
                                    }
                                  }}
                                />
                                <Typography variant="caption" color="text.secondary" ml={1}>
                                  {calculateUtilization(card.usedCredit, card.limit)}%
                                </Typography>
                              </Box>
                            </Box>
                            
                            <Box display="flex" justifyContent="space-between">
                              <Typography variant="body2" color="text.secondary">Credit Limit:</Typography>
                              <Typography variant="body2">${card.limit?.toLocaleString()}</Typography>
                            </Box>
                            
                            {card.rewards && (
                              <Box display="flex" justifyContent="space-between">
                                <Typography variant="body2" color="text.secondary">Reward Points:</Typography>
                                <Chip 
                                  size="small" 
                                  label={`${card.rewards.toLocaleString()} pts`}
                                  color="primary"
                                  variant="outlined"
                                />
                              </Box>
                            )}
                          </Stack>

                          {activeCardId === card.id && card.transactions && card.transactions.length > 0 && (
                            <>
                              <Divider sx={{ my: 2 }} />
                              <Typography variant="subtitle2" gutterBottom>
                                Recent Transactions
                              </Typography>
                              <Stack spacing={1}>
                                {card.transactions.map(transaction => (
                                  <Box 
                                    key={transaction.id}
                                    sx={{ 
                                      display: 'flex', 
                                      justifyContent: 'space-between', 
                                      p: 1,
                                      borderRadius: 1,
                                      '&:hover': { bgcolor: 'grey.50' }
                                    }}
                                  >
                                    <Box>
                                      <Typography variant="body2">{transaction.merchant}</Typography>
                                      <Typography variant="caption" color="text.secondary">
                                        {new Date(transaction.date).toLocaleDateString()} · {transaction.category}
                                      </Typography>
                                    </Box>
                                    <Typography variant="body2" fontWeight="500">
                                      -${transaction.amount.toFixed(2)}
                                    </Typography>
                                  </Box>
                                ))}
                              </Stack>
                            </>
                          )}
                        </>
                      )}
                      
                      {card.type === 'Debit' && (
                        <Stack spacing={1}>
                          <Box display="flex" justifyContent="space-between">
                            <Typography variant="body2" color="text.secondary">Current Balance:</Typography>
                            <Typography variant="body2" fontWeight="500">${card.balance?.toLocaleString()}</Typography>
                          </Box>
                        </Stack>
                      )}
                      
                      <Stack 
                        direction="row" 
                        spacing={1} 
                        justifyContent="flex-end" 
                        mt={2}
                      >
                        <Tooltip title="Report Lost or Stolen">
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={(e) => handleReportLost(card.id, e)}
                          >
                            <SecurityIcon />
                          </IconButton>
                        </Tooltip>
                        
                        {card.type === 'Credit' && (
                          <Tooltip title="Request Limit Increase">
                            <IconButton 
                              size="small"
                              color="primary"
                              onClick={(e) => handleRequestLimit(card.id, e)}
                            >
                              <TrendingUpIcon />
                            </IconButton>
                          </Tooltip>
                        )}
                      </Stack>
                    </CardContent>
                  </Paper>
                </Box>
              </Grid>
            ))}
          </Grid>
          
          {getFilteredCards().length === 0 && (
            <Alert severity="info" sx={{ mt: 2 }}>
              No cards found in this category. {tabValue === 3 && "All your cards have been activated."}
            </Alert>
          )}
        </TabPanel>
      </Paper>

      {/* Lock/Unlock Card Dialog */}
      <Dialog open={lockCardDialogOpen} onClose={closeLockCardDialog} maxWidth="xs" fullWidth>
        <DialogTitle>
          {cards.find(c => c.id === selectedCard)?.status === 'Temporarily Locked' ? 'Unlock Card' : 'Lock Card'}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            {cards.find(c => c.id === selectedCard)?.status === 'Temporarily Locked' ? 
              'Are you sure you want to unlock your card ending in ' :
              'Are you sure you want to temporarily lock your card ending in '
            }
            <strong>{cards.find(c => c.id === selectedCard)?.lastFour}</strong>?
            <br /><br />
            {cards.find(c => c.id === selectedCard)?.status === 'Temporarily Locked' ? 
              'Unlocking will allow transactions to be processed again.' :
              'Temporarily locking your card will prevent any new transactions until you unlock it.'
            }
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeLockCardDialog}>Cancel</Button>
          <Button onClick={closeLockCardDialog} variant="contained" color="primary" autoFocus>
            {cards.find(c => c.id === selectedCard)?.status === 'Temporarily Locked' ? 'Unlock Card' : 'Lock Card'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Report Lost Card Dialog */}
      <Dialog open={reportLostDialogOpen} onClose={closeReportLostDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Report Lost or Stolen Card</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Report your card ending in <strong>{cards.find(c => c.id === selectedCard)?.lastFour}</strong> as lost or stolen.
            <br /><br />
            This will permanently deactivate this card and we'll send you a replacement.
          </DialogContentText>
          <FormControl fullWidth margin="dense">
            <InputLabel>Reason</InputLabel>
            <Select defaultValue="lost">
              <MenuItem value="lost">Lost card</MenuItem>
              <MenuItem value="stolen">Stolen card</MenuItem>
              <MenuItem value="damaged">Damaged card</MenuItem>
              <MenuItem value="fraud">Suspicious activity</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Additional Information"
            fullWidth
            multiline
            rows={3}
          />
          <FormControlLabel
            control={<Switch color="primary" />}
            label="Rush delivery (additional fee applies)"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={closeReportLostDialog}>Cancel</Button>
          <Button 
            onClick={closeReportLostDialog} 
            variant="contained" 
            color="error" 
            startIcon={<WarningIcon />}
            autoFocus
          >
            Report and Replace
          </Button>
        </DialogActions>
      </Dialog>

      {/* Request Credit Limit Dialog */}
      <Dialog open={requestLimitDialogOpen} onClose={closeRequestLimitDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Request Credit Limit Change</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Request a credit limit change for your card ending in <strong>{cards.find(c => c.id === selectedCard)?.lastFour}</strong>.
            <br /><br />
            Current limit: <strong>${cards.find(c => c.id === selectedCard)?.limit?.toLocaleString()}</strong>
          </DialogContentText>
          <TextField
            margin="dense"
            label="Requested Limit"
            fullWidth
            type="number"
            inputProps={{ min: 1000, step: 1000 }}
            defaultValue={cards.find(c => c.id === selectedCard)?.limit}
          />
          <TextField
            margin="dense"
            label="Annual Income"
            fullWidth
            type="number"
            inputProps={{ min: 0, step: 1000 }}
            helperText="This helps us evaluate your request"
          />
          <TextField
            margin="dense"
            label="Reason for Increase (Optional)"
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={closeRequestLimitDialog}>Cancel</Button>
          <Button 
            onClick={closeRequestLimitDialog} 
            variant="contained" 
            color="primary" 
            startIcon={<TrendingUpIcon />}
          >
            Submit Request
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Request New Card Dialog */}
      <Dialog open={newCardDialogOpen} onClose={closeNewCardDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Request New Card</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Select the type of card you'd like to apply for. Our team will review your application and contact you.
          </DialogContentText>
          
          <FormControl fullWidth margin="dense">
            <InputLabel>Card Type</InputLabel>
            <Select defaultValue="credit">
              <MenuItem value="credit">Credit Card</MenuItem>
              <MenuItem value="debit">Debit Card</MenuItem>
              <MenuItem value="prepaid">Prepaid Card</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth margin="dense">
            <InputLabel>Card Product</InputLabel>
            <Select defaultValue="rewards">
              <MenuItem value="rewards">Cash Rewards Card</MenuItem>
              <MenuItem value="travel">Premium Travel Card</MenuItem>
              <MenuItem value="secured">Secured Credit Card</MenuItem>
              <MenuItem value="business">Business Credit Card</MenuItem>
            </Select>
          </FormControl>
          
          <FormControlLabel
            control={<Switch color="primary" />}
            label="Request virtual card (available immediately)"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={closeNewCardDialog}>Cancel</Button>
          <Button 
            onClick={closeNewCardDialog} 
            variant="contained" 
            color="primary" 
            startIcon={<CreditCardIcon />}
          >
            Submit Application
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default CardManagement; 