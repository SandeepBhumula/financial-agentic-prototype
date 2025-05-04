import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  TextField, 
  IconButton, 
  Avatar,
  CircularProgress,
  Card,
  CardContent,
  CardHeader,
  Divider,
  InputAdornment
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import { chatService, checkApiStatus } from '../services/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatAssistantProps {
  embedded?: boolean;
}

const ChatAssistant: React.FC<ChatAssistantProps> = ({ embedded = false }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! How can I help you with your financial questions today?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [apiAvailable, setApiAvailable] = useState<boolean>(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check if API is available on component mount
  useEffect(() => {
    const checkApiAvailability = async () => {
      console.log('[CHAT] Checking API availability...');
      try {
        const available = await checkApiStatus();
        console.log('[CHAT] API available:', available);
        setApiAvailable(available);
      } catch (error) {
        console.error('[CHAT] Error checking API status:', error);
        setApiAvailable(false);
      }
    };

    checkApiAvailability();
  }, []);

  // Scroll to bottom of messages when new ones arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const sendMessage = async () => {
    if (input.trim() === '') return;

    // Add user message to chat
    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      if (!apiAvailable) {
        throw new Error("API is not available");
      }

      // Use the chatService which has the correct endpoint
      const data = await chatService.sendChatQuery(input);
      
      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.success ? data.response : 
                "Sorry, there was an error processing your request.",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I couldn\'t connect to the financial agent service. Please try again later.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Chat bubble component
  const ChatBubble: React.FC<{ message: Message }> = ({ message }) => {
    const isUser = message.role === 'user';
    
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2,
        }}
      >
        {!isUser && (
          <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>AI</Avatar>
        )}
        <Paper
          elevation={1}
          sx={{
            p: 2,
            maxWidth: '75%',
            backgroundColor: isUser ? 'primary.main' : 'background.paper',
            color: isUser ? 'white' : 'text.primary',
            borderRadius: 2,
          }}
        >
          <Typography variant="body1">{message.content}</Typography>
          <Typography variant="caption" color={isUser ? 'white' : 'text.secondary'} sx={{ display: 'block', mt: 1 }}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Typography>
        </Paper>
        {isUser && (
          <Avatar sx={{ bgcolor: 'secondary.main', ml: 1 }}>ME</Avatar>
        )}
      </Box>
    );
  };

  if (embedded) {
    return (
      <Card elevation={3} sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column', 
        maxHeight: embedded ? '100%' : 500 
      }}>
        <CardHeader
          avatar={<AccountBalanceWalletIcon color="primary" />}
          title="Financial Assistant"
          sx={{ 
            backgroundColor: 'primary.light', 
            color: 'white',
            '& .MuiCardHeader-title': { color: 'white' }
          }}
        />
        <Divider />
        <CardContent sx={{ p: 2, flexGrow: 1, overflowY: 'auto', bgcolor: 'grey.50' }}>
          {messages.map((msg, index) => (
            <ChatBubble key={index} message={msg} />
          ))}
          <div ref={messagesEndRef} />
          
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <CircularProgress size={24} />
            </Box>
          )}
        </CardContent>
        <Divider />
        <Box sx={{ p: 2, backgroundColor: 'background.paper' }}>
          <TextField
            fullWidth
            placeholder="Ask me about your finances..."
            variant="outlined"
            size="small"
            value={input}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton 
                    color="primary" 
                    onClick={sendMessage} 
                    disabled={isLoading || input.trim() === ''}
                    edge="end"
                  >
                    <SendIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </Box>
      </Card>
    );
  }

  return null; // We're not using the floating version anymore
};

export default ChatAssistant; 