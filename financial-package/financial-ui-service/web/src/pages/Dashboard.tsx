import React from 'react';
import { 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Divider, 
  List, 
  ListItem, 
  ListItemText, 
  Button, 
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Chip,
  useTheme,
  useMediaQuery
} from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import SavingsIcon from '@mui/icons-material/Savings';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import { Link as RouterLink } from 'react-router-dom';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';
import ChatAssistant from '../components/ChatAssistant';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title);

// Mock data
const accountBalance = 4523.65;
const availableCredit = 7500;
const savingsBalance = 12750.42;

// Added health spending account balances
const hsaBalance = 3250.75;
const fsaBalance = 1850.00;
const prepaidCardBalance = 500.00;
const healthcareSpendBalance = 2100.50;

const recentTransactions = [
  // Added transactions for different account types
  { id: 1, merchant: 'Starbucks', amount: 42.50, date: '2023-06-12', type: 'debit', category: 'Dining', account: 'Checking' },
  { id: 2, merchant: 'Amazon', amount: 156.78, date: '2023-06-10', type: 'debit', category: 'Shopping', account: 'Credit Card' },
  { id: 3, merchant: 'Salary Deposit', amount: 3500.00, date: '2023-06-01', type: 'credit', category: 'Income', account: 'Checking' },
  { id: 4, merchant: 'City Hospital', amount: 125.00, date: '2023-06-08', type: 'debit', category: 'Healthcare', account: 'HSA' },
  { id: 5, merchant: 'Pharmacy Plus', amount: 45.75, date: '2023-06-05', type: 'debit', category: 'Healthcare', account: 'FSA' },
  { id: 6, merchant: 'Dental Care', amount: 210.00, date: '2023-05-30', type: 'debit', category: 'Healthcare', account: 'HSA' },
  { id: 7, merchant: 'Vision Center', amount: 175.25, date: '2023-05-28', type: 'debit', category: 'Healthcare', account: 'Prepaid Card' },
  { id: 8, merchant: 'Target', amount: 87.32, date: '2023-05-25', type: 'debit', category: 'Shopping', account: 'Credit Card' },
];

const cards = [
  { 
    id: 1, 
    name: 'Cash Rewards Credit Card', 
    lastFour: '1234', 
    expiryDate: '05/25', 
    availableCredit: 7500,
    usedCredit: 2500,
    status: 'Active'
  },
  { 
    id: 2, 
    name: 'Premium Travel Card', 
    lastFour: '5678', 
    expiryDate: '09/26', 
    availableCredit: 15000,
    usedCredit: 4200,
    status: 'Active'
  },
  { 
    id: 3, 
    name: 'Health Savings Debit', 
    lastFour: '9012', 
    expiryDate: '12/24', 
    balance: 2340.75,
    status: 'Pending Activation'
  },
];

// Updated spending by category data for doughnut chart
const spendingData = {
  labels: ['Dining', 'Shopping', 'Transport', 'Utilities', 'Entertainment', 'Healthcare'],
  datasets: [
    {
      label: 'Spending by Category',
      data: [340, 780, 490, 320, 280, 560], // Added healthcare spending
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(76, 175, 80, 0.7)', // Green for healthcare
      ],
      borderWidth: 1,
    },
  ],
};

// Spending trend data (for line chart)
const trendData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Monthly Spending',
      data: [1258, 1340, 1560, 1890, 2110, 1950],
      borderColor: 'rgba(54, 162, 235, 0.7)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.3,
    },
    {
      label: 'Healthcare Spending',
      data: [320, 410, 380, 520, 490, 560],
      borderColor: 'rgba(76, 175, 80, 0.7)',
      backgroundColor: 'rgba(76, 175, 80, 0.2)',
      tension: 0.3,
    },
  ],
};

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary.dark">
        Financial Dashboard
      </Typography>
      
      {/* Health Accounts Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <HealthAndSafetyIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                HSA Balance
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${hsaBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <ArrowUpwardIcon sx={{ mr: 1, fontSize: 16 }} />
              <Typography variant="body2">Tax-advantaged health savings</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #26a69a 0%, #00796b 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <LocalHospitalIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                FSA Balance
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${fsaBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <ArrowDownwardIcon sx={{ mr: 1, fontSize: 16 }} />
              <Typography variant="body2">Use it before year-end</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #1976d2 0%, #0d47a1 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <CreditCardIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                Prepaid Card
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${prepaidCardBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2">Healthcare prepaid balance</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #7b1fa2 0%, #4a148c 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <AccountBalanceWalletIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                Healthcare Spend
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${healthcareSpendBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2">YTD healthcare expenses</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      {/* Regular Account Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #f57c00 0%, #e65100 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <AccountBalanceIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                Account Balance
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${accountBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <ArrowUpwardIcon sx={{ mr: 1, fontSize: 16 }} />
              <Typography variant="body2">3.5% from last month</Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #ef5350 0%, #c62828 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <CreditCardIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                Available Credit
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${availableCredit.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <ArrowDownwardIcon sx={{ mr: 1, fontSize: 16 }} />
              <Typography variant="body2">$500 used this month</Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              background: 'linear-gradient(135deg, #5c6bc0 0%, #3949ab 100%)',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <SavingsIcon sx={{ mr: 1 }} />
              <Typography component="h2" variant="h6" fontWeight="500">
                Savings Balance
              </Typography>
            </Box>
            <Typography component="p" variant="h4" fontWeight="bold">
              ${savingsBalance.toLocaleString()}
            </Typography>
            <Box sx={{ mt: 'auto', display: 'flex', alignItems: 'center' }}>
              <ArrowUpwardIcon sx={{ mr: 1, fontSize: 16 }} />
              <Typography variant="body2">12.3% from last year</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Left Column - Financial Data */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={3}>
            {/* Recent Transactions */}
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 0, borderRadius: 2, overflow: 'hidden' }}>
                <CardHeader
                  title="Recent Transactions"
                  action={
                    <Button size="small" color="primary">
                      View All
                    </Button>
                  }
                  sx={{ bgcolor: 'grey.50', borderBottom: 1, borderColor: 'divider', p: 2 }}
                />
                <List sx={{ p: 0 }}>
                  {recentTransactions.map((transaction) => (
                    <ListItem key={transaction.id} divider sx={{ py: 2 }}>
                      <Avatar 
                        sx={{ 
                          bgcolor: transaction.type === 'credit' ? 'success.light' : 'primary.light',
                          mr: 2
                        }}
                      >
                        {transaction.type === 'credit' ? <ArrowUpwardIcon /> : <ArrowDownwardIcon />}
                      </Avatar>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center">
                            {transaction.merchant}
                            <Chip 
                              label={transaction.category} 
                              size="small" 
                              sx={{ ml: 1, fontSize: '0.7rem' }}
                              variant="outlined"
                            />
                          </Box>
                        }
                        secondary={
                          <Box display="flex" alignItems="center">
                            <Typography variant="caption">{new Date(transaction.date).toLocaleDateString()}</Typography>
                            <Chip 
                              label={transaction.account} 
                              size="small" 
                              sx={{ ml: 1, fontSize: '0.7rem' }}
                              color={
                                transaction.account === 'HSA' ? 'success' :
                                transaction.account === 'FSA' ? 'info' :
                                transaction.account === 'Prepaid Card' ? 'secondary' :
                                'default'
                              }
                              variant="outlined"
                            />
                          </Box>
                        }
                      />
                      <Typography
                        variant="body1"
                        sx={{
                          color: transaction.type === 'credit' ? 'success.main' : 'text.primary',
                          fontWeight: 'bold',
                        }}
                      >
                        {transaction.type === 'credit' ? '+' : '-'}${transaction.amount.toFixed(2)}
                      </Typography>
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            {/* Spending Trend Chart */}
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <TrendingUpIcon sx={{ color: 'primary.main', mr: 1 }} />
                  <Typography variant="h6" fontWeight="500">
                    Spending Trend
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
                <Box sx={{ height: 300 }}>
                  <Line 
                    data={trendData} 
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top' as const,
                        },
                        title: {
                          display: true,
                          text: '6-Month Spending Trend'
                        },
                      },
                    }} 
                  />
                </Box>
              </Paper>
            </Grid>
            
            {/* Spending Category Chart (mobile only) */}
            {isMobile && (
              <Grid item xs={12}>
                <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
                  <Typography variant="h6" fontWeight="500" gutterBottom>
                    Spending by Category
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  <Box sx={{ height: 240 }}>
                    <Doughnut 
                      data={spendingData} 
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                      }} 
                    />
                  </Box>
                </Paper>
              </Grid>
            )}
          </Grid>
        </Grid>
        
        {/* Right Column - Chat and Cards */}
        <Grid item xs={12} md={4}>
          <Grid container spacing={3}>
            {/* Financial Assistant */}
            <Grid item xs={12}>
              <Box sx={{ height: isMobile ? 'auto' : 400 }}>
                <ChatAssistant embedded={true} />
              </Box>
            </Grid>
            
            {/* Spending Category Chart (desktop only) */}
            {!isMobile && (
              <Grid item xs={12}>
                <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
                  <Typography variant="h6" fontWeight="500" gutterBottom>
                    Spending by Category
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  <Box sx={{ height: 240 }}>
                    <Doughnut 
                      data={spendingData} 
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                      }} 
                    />
                  </Box>
                </Paper>
              </Grid>
            )}
            
            {/* My Cards Quick Access */}
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 0, borderRadius: 2, overflow: 'hidden' }}>
                <CardHeader
                  title="Quick Card Access"
                  action={
                    <Button 
                      component={RouterLink} 
                      to="/cards" 
                      size="small"
                      color="primary"
                    >
                      View All Cards
                    </Button>
                  }
                  sx={{ bgcolor: 'grey.50', borderBottom: 1, borderColor: 'divider', p: 2 }}
                />
                <CardContent sx={{ p: 2 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      flexDirection: 'column',
                      gap: 2,
                      p: 2,
                    }}
                  >
                    <Button
                      variant="contained"
                      color="primary"
                      component={RouterLink}
                      to="/cards"
                      startIcon={<CreditCardIcon />}
                      fullWidth
                      sx={{ py: 1 }}
                    >
                      Manage Cards
                    </Button>
                    <Button
                      variant="outlined"
                      color="warning"
                      component={RouterLink}
                      to="/activate"
                      startIcon={<CreditCardIcon />}
                      fullWidth
                      sx={{ py: 1 }}
                    >
                      Activate New Card
                    </Button>
                  </Box>
                </CardContent>
              </Paper>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard; 