// API response interface
interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

/**
 * Chat API Services
 */
export const chatService = {
  /**
   * Send a query to the chat assistant
   */
  sendChatQuery: async (query: string): Promise<ChatResponse> => {
    try {
      // Use the correct chat endpoint
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query })
      });
      
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error sending chat query:', error);
      return {
        response: 'Sorry, there was an error processing your request.',
        success: false,
        error: 'Network error or service unavailable'
      };
    }
  },
};

/**
 * Check API status
 */
export const checkApiStatus = async (): Promise<boolean> => {
  try {
    const response = await fetch('/');
    return response.ok;
  } catch (error) {
    console.error('API connection error:', error);
    return false;
  }
};

export default {
  chat: chatService,
  checkApiStatus
}; 