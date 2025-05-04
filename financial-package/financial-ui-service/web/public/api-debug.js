/**
 * API debugging utilities
 * 
 * To use this script:
 * 1. Open your browser to http://localhost:2025
 * 2. Open the browser console (F12)
 * 3. Copy and paste the following line:
 *    fetch('/api-debug.js').then(r => r.text()).then(t => eval(t))
 */

console.log("API Debug Tools loaded!");

// Test the chat endpoint directly
async function testChatDirect(message = "Hello") {
  console.log(`Testing direct chat endpoint with message: "${message}"`);
  
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: message })
    });
    
    const status = response.status;
    const data = await response.json();
    
    console.log(`Chat endpoint response (status ${status}):`, data);
    return { status, data };
  } catch (error) {
    console.error("Error calling chat endpoint:", error);
    return { error: error.message };
  }
}

// Override fetch for debugging
const originalFetch = window.fetch;
window.fetch = async function(url, options) {
  const startTime = new Date().getTime();
  console.log(`[FETCH] ${options?.method || 'GET'} ${url}`, options);
  
  try {
    const response = await originalFetch(url, options);
    const endTime = new Date().getTime();
    const duration = endTime - startTime;
    
    // Clone the response so we can read its body
    const clonedResponse = response.clone();
    let responseData;
    try {
      responseData = await clonedResponse.text();
      try {
        // Try to parse as JSON
        responseData = JSON.parse(responseData);
      } catch (e) {
        // Not JSON, keep as text
      }
    } catch (e) {
      responseData = "<Unable to read response body>";
    }
    
    console.log(`[FETCH] Response ${response.status} (${duration}ms):`, responseData);
    return response;
  } catch (error) {
    console.error(`[FETCH] Error:`, error);
    throw error;
  }
};

// Monkey patch the chatService to log and fix endpoint issues
function monkeyPatchChatService() {
  if (typeof chatService !== 'undefined') {
    console.log("Found chatService, patching sendChatQuery method...");
    
    const originalSendChatQuery = chatService.sendChatQuery;
    
    chatService.sendChatQuery = async function(query) {
      console.log("PATCHED sendChatQuery called with:", query);
      
      try {
        // Use the correct endpoint directly
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
        
        const data = await response.json();
        console.log("Patched chat response:", data);
        return data;
      } catch (error) {
        console.error("Error in patched sendChatQuery:", error);
        return {
          response: 'Sorry, there was an error processing your request.',
          success: false,
          error: 'Network error or service unavailable'
        };
      }
    };
    
    console.log("Chat service patched successfully!");
    return true;
  } else {
    console.error("chatService not found in global scope!");
    return false;
  }
}

// Helper to check localStorage
function checkLocalStorage() {
  console.log("Checking localStorage for cached values:");
  
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    const value = localStorage.getItem(key);
    console.log(`${key}: ${value.substring(0, 100)}${value.length > 100 ? '...' : ''}`);
  }
}

// Clear browser cache for this site
function clearSiteCache() {
  console.log("Clearing localStorage...");
  localStorage.clear();
  
  if ('caches' in window) {
    console.log("Clearing Cache API...");
    caches.keys().then(names => {
      names.forEach(name => {
        caches.delete(name);
      });
    });
  }
  
  console.log("Cache cleared. You should refresh the page now.");
}

// Make functions available globally
window.apiDebug = {
  testChatDirect,
  monkeyPatchChatService,
  checkLocalStorage,
  clearSiteCache
};

console.log("API Debug utilities ready! Available commands:");
console.log("- apiDebug.testChatDirect('Your message')");
console.log("- apiDebug.monkeyPatchChatService()");
console.log("- apiDebug.checkLocalStorage()");
console.log("- apiDebug.clearSiteCache()"); 