import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Button,
  TextField,
  Grid,
  Card,
  CardContent,
  FormControl,
  FormControlLabel,
  RadioGroup,
  Radio,
  Checkbox,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import SecurityIcon from '@mui/icons-material/Security';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';

// Mock cards pending activation
const pendingCards = [
  {
    id: 3,
    name: 'Health Savings Debit',
    type: 'Debit',
    lastFour: '9012',
    expiryDate: '12/24',
    status: 'Pending Activation',
    isVirtual: true,
    cardHolder: 'John Smith'
  }
];

// Card color mapping
const cardColors: {[key: string]: {background: string, text: string}} = {
  'Credit': {
    background: 'linear-gradient(135deg, #2196f3 0%, #0d47a1 100%)',
    text: '#ffffff'
  },
  'Debit': {
    background: 'linear-gradient(135deg, #4caf50 0%, #1b5e20 100%)',
    text: '#ffffff'
  },
  'Prepaid': {
    background: 'linear-gradient(135deg, #ff9800 0%, #e65100 100%)',
    text: '#ffffff'
  }
};

// Stepper steps
const steps = ['Select Card', 'Verify Information', 'Activate Card'];

const StyledCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  margin: theme.spacing(1),
  height: 200,
  borderRadius: theme.spacing(1),
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'scale(1.02)',
    boxShadow: theme.shadows[8],
    cursor: 'pointer'
  }
}));

const SelectedCardIndicator = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: -10,
  right: -10,
  background: theme.palette.success.main,
  borderRadius: '50%',
  padding: theme.spacing(0.5),
  color: theme.palette.common.white,
  width: 32,
  height: 32,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  border: `2px solid ${theme.palette.common.white}`,
  zIndex: 2
}));

const CardActivation: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedCard, setSelectedCard] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    cvv: '',
    email: '',
    phoneNumber: '',
    agreeToTerms: false
  });
  const [activating, setActivating] = useState(false);
  const [activationComplete, setActivationComplete] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSelectCard = (cardId: number) => {
    setSelectedCard(cardId);
  };

  const handleNext = () => {
    if (activeStep === 0 && !selectedCard) {
      setErrorMessage('Please select a card to activate');
      return;
    }

    if (activeStep === 1) {
      // Validate form
      if (!formData.cvv) {
        setErrorMessage('Please enter the CVV/security code');
        return;
      }
      if (formData.cvv.length < 3) {
        setErrorMessage('CVV must be at least 3 digits');
        return;
      }
      if (!formData.email) {
        setErrorMessage('Please enter your email');
        return;
      }
      if (!formData.agreeToTerms) {
        setErrorMessage('You must agree to the terms and conditions');
        return;
      }
    }

    if (activeStep === 2) {
      // Activate card
      setActivating(true);
      setErrorMessage(null);
      // Simulate API call
      setTimeout(() => {
        setActivating(false);
        setActivationComplete(true);
      }, 2000);
      return;
    }

    setErrorMessage(null);
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
    setErrorMessage(null);
  };

  const handleFormChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked, type } = event.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleDone = () => {
    navigate('/cards');
  };

  // Get the selected card object
  const cardData = pendingCards.find(c => c.id === selectedCard);

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom align="center">
          Card Activation
        </Typography>
        
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        
        {errorMessage && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {errorMessage}
          </Alert>
        )}

        {/* Step 1: Select Card */}
        {activeStep === 0 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Select a card to activate
            </Typography>
            <Grid container spacing={3}>
              {pendingCards.map((card) => (
                <Box 
                  key={card.id}
                  sx={{ 
                    width: { xs: '100%', sm: '50%' }, 
                    p: 1.5 
                  }}
                >
                  <Box position="relative">
                    {selectedCard === card.id && (
                      <SelectedCardIndicator>
                        <CheckCircleOutlineIcon fontSize="small" />
                      </SelectedCardIndicator>
                    )}
                    <StyledCard 
                      elevation={selectedCard === card.id ? 8 : 3}
                      onClick={() => handleSelectCard(card.id)}
                      sx={{
                        background: cardColors[card.type].background,
                        color: cardColors[card.type].text,
                        border: selectedCard === card.id ? '2px solid #4caf50' : 'none'
                      }}
                    >
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                          <Typography variant="h6" component="div" sx={{ mb: 2 }}>
                            {card.name}
                          </Typography>
                          {card.isVirtual && (
                            <Box 
                              sx={{ 
                                bgcolor: 'rgba(255,255,255,0.2)', 
                                color: 'inherit',
                                px: 1,
                                py: 0.5,
                                borderRadius: 1,
                                fontSize: '0.75rem',
                                fontWeight: 'bold'
                              }}
                            >
                              Virtual
                            </Box>
                          )}
                        </Box>

                        <Typography variant="body1">
                          •••• •••• •••• {card.lastFour}
                        </Typography>

                        <Typography variant="body2" sx={{ mt: 1 }}>
                          Expires: {card.expiryDate}
                        </Typography>
                        
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          {card.cardHolder}
                        </Typography>

                        <Box sx={{ position: 'absolute', bottom: 20, left: 16, display: 'flex', alignItems: 'center' }}>
                          <Box sx={{ mr: 1, display: 'flex', alignItems: 'center' }}>
                            {card.type === 'Credit' ? 
                              <CreditCardIcon fontSize="small" /> : 
                              <AccountBalanceWalletIcon fontSize="small" />
                            }
                          </Box>
                          <Typography variant="body2">
                            {card.type} Card
                          </Typography>
                        </Box>
                      </CardContent>
                    </StyledCard>
                  </Box>
                </Box>
              ))}
              
              {pendingCards.length === 0 && (
                <Box sx={{ width: '100%', p: 1.5 }}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="subtitle1" color="text.secondary">
                      You don't have any cards pending activation.
                    </Typography>
                    <Button 
                      component={RouterLink} 
                      to="/cards" 
                      variant="contained" 
                      sx={{ mt: 2 }}
                    >
                      View All Cards
                    </Button>
                  </Paper>
                </Box>
              )}
            </Grid>
          </Box>
        )}

        {/* Step 2: Verify Information */}
        {activeStep === 1 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Verify Card Information
            </Typography>
            
            <Grid container spacing={3}>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  required
                  name="cvv"
                  label="CVV/Security Code"
                  type="password"
                  value={formData.cvv}
                  onChange={handleFormChange}
                  fullWidth
                  margin="normal"
                  inputProps={{ maxLength: 4 }}
                  helperText="3-4 digit code on the back of your card"
                />
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  disabled
                  label="Card Number"
                  value={`•••• •••• •••• ${cardData?.lastFour}`}
                  fullWidth
                  margin="normal"
                />
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  disabled
                  label="Expiry Date"
                  value={cardData?.expiryDate}
                  fullWidth
                  margin="normal"
                />
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  disabled
                  label="Card Holder"
                  value={cardData?.cardHolder}
                  fullWidth
                  margin="normal"
                />
              </Box>
              <Box sx={{ width: '100%', p: 1.5 }}>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle1" gutterBottom>
                  Contact Information
                </Typography>
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  required
                  name="email"
                  label="Email Address"
                  type="email"
                  value={formData.email}
                  onChange={handleFormChange}
                  fullWidth
                  margin="normal"
                  helperText="We'll send a confirmation email"
                />
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' }, p: 1.5 }}>
                <TextField
                  name="phoneNumber"
                  label="Phone Number (Optional)"
                  value={formData.phoneNumber}
                  onChange={handleFormChange}
                  fullWidth
                  margin="normal"
                />
              </Box>
              <Box sx={{ width: '100%', p: 1.5 }}>
                <FormControlLabel
                  control={
                    <Checkbox
                      name="agreeToTerms"
                      checked={formData.agreeToTerms}
                      onChange={handleFormChange}
                      color="primary"
                    />
                  }
                  label={
                    <Typography variant="body2">
                      I agree to the terms and conditions and acknowledge that activating this card will make it ready for immediate use.
                    </Typography>
                  }
                />
              </Box>
            </Grid>
          </Box>
        )}

        {/* Step 3: Confirmation */}
        {activeStep === 2 && !activationComplete && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6" gutterBottom>
              Ready to Activate Your Card
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
              <Box sx={{ 
                width: 300, 
                height: 180, 
                background: cardColors[cardData?.type || 'Credit'].background,
                borderRadius: 2,
                position: 'relative',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                p: 2,
                color: '#fff',
                boxShadow: 3
              }}>
                <Typography variant="subtitle1">{cardData?.name}</Typography>
                <Typography variant="body1" sx={{ my: 2 }}>•••• •••• •••• {cardData?.lastFour}</Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2">{cardData?.cardHolder}</Typography>
                  <Typography variant="body2">{cardData?.expiryDate}</Typography>
                </Box>
              </Box>
            </Box>
            
            <Typography variant="body1" paragraph>
              Please confirm that you want to activate the card ending in <strong>{cardData?.lastFour}</strong>.
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Once activated, your {cardData?.type.toLowerCase()} card will be ready for immediate use.
              {cardData?.type === 'Debit' && " You can use it for in-store purchases, online shopping, and ATM withdrawals."}
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <SecurityIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Your activation is secure and encrypted
              </Typography>
            </Box>
          </Box>
        )}

        {/* Activation Complete */}
        {activationComplete && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center' }}>
              <CheckCircleOutlineIcon sx={{ fontSize: 64, color: 'success.main' }} />
            </Box>
            <Typography variant="h5" gutterBottom>
              Card Successfully Activated!
            </Typography>
            <Typography variant="body1" paragraph>
              Your {cardData?.name} ending in {cardData?.lastFour} has been activated and is ready to use.
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              A confirmation has been sent to your email address.
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleDone}
              sx={{ mt: 2 }}
            >
              Go to My Cards
            </Button>
          </Box>
        )}

        {/* Navigation buttons */}
        {!activationComplete && (
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Back
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={handleNext}
              disabled={activating}
              startIcon={activating ? <CircularProgress size={16} /> : undefined}
            >
              {activeStep === steps.length - 1 ? 'Activate Card' : 'Next'}
            </Button>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default CardActivation; 