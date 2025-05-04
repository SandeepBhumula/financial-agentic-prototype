/**
 * API Debugging Utility - Run in browser console
 * 
 * To use this script, open your browser console and type:
 * loadApiDebugger()
 * 
 * Then use one of the test functions:
 * debug.testRoot()     - Test root endpoint
 * debug.testChat()     - Test chat endpoint with sample message
 * debug.testRaw()      - Test direct fetch to the endpoints
 * debug.getNetworkInfo() - Get network configuration info
 */

// Function to load the debugger into the window context
function loadApiDebugger() {
  console.log("API Debugger loaded! Use debug.* functions to test API connectivity");
  
  // Create debugging object in window scope
  window.debug = {
    // Test the root endpoint
    testRoot: async function() {
      console.log("🔍 Testing API root endpoint...");
      try {
        // Test both root paths to verify which one works
        const rootResponse = await fetch('/');
        console.log("✅ Direct root endpoint status:", rootResponse.status);
        const rootData = await rootResponse.text();
        console.log("Direct root response:", rootData);
        
        const apiRootResponse = await fetch('/api/');
        console.log("✅ API root endpoint status:", apiRootResponse.status);
        const apiRootData = await apiRootResponse.text();
        console.log("API root response:", apiRootData);
        
        return { 
          root: { status: rootResponse.status, data: rootData },
          apiRoot: { status: apiRootResponse.status, data: apiRootData }
        };
      } catch (error) {
        console.error("❌ API Root Error:", error);
        return { error };
      }
    },
    
    // Test the chat endpoint
    testChat: async function(message = "Test message") {
      console.log(`🔍 Testing API chat endpoint with message: "${message}"...`);
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: message })
        });
        console.log("✅ API Chat Status:", response.status);
        const data = await response.json();
        console.log("Response data:", data);
        return { status: response.status, data };
      } catch (error) {
        console.error("❌ API Chat Error:", error);
        return { error };
      }
    },
    
    // Test direct connections to raw endpoints
    testRaw: async function() {
      console.log("🔍 Testing direct API connections...");
      const results = {};
      
      // Test various possible API endpoints
      const endpoints = [
        '/',                   // Root via Nginx proxy to agent API
        '/api/',               // API root via Nginx
        '/api/chat',           // API chat endpoint via Nginx
        'http://localhost:8000/',          // Direct to agent API
        'http://localhost:8000/api/',      // Direct to agent API with /api/ path
        'http://localhost:8000/api/chat'   // Direct to agent API chat
      ];
      
      for (const url of endpoints) {
        try {
          console.log(`Testing: ${url}`);
          const response = await fetch(url, { 
            method: url.includes('/chat') ? 'POST' : 'GET',
            headers: url.includes('/chat') ? {'Content-Type': 'application/json'} : {},
            body: url.includes('/chat') ? JSON.stringify({ query: "Test" }) : undefined
          });
          
          const text = await response.text();
          results[url] = { 
            status: response.status, 
            text: text.substring(0, 100) + (text.length > 100 ? '...' : '') 
          };
          console.log(`✅ ${url} - Status: ${response.status}`);
        } catch (error) {
          results[url] = { error: error.message };
          console.error(`❌ ${url} - Error: ${error.message}`);
        }
      }
      
      console.table(results);
      return results;
    },
    
    // Test the chat component
    testChatComponent: async function(message = "Test message") {
      console.log(`🔍 Testing chat component with message: "${message}"...`);
      
      // Find chatService in the global scope
      if (typeof chatService !== 'undefined') {
        try {
          console.log("Found chatService in global scope, attempting to call sendChatQuery");
          const response = await chatService.sendChatQuery(message);
          console.log("✅ Chat Component Test Response:", response);
          return response;
        } catch (error) {
          console.error("❌ Chat Component Test Error:", error);
          return { error };
        }
      } else {
        console.error("❌ chatService not found in global scope");
        return { error: "chatService not found" };
      }
    },
    
    // Get network information
    getNetworkInfo: function() {
      console.log("🔍 Gathering network configuration info...");
      const info = {
        currentLocation: window.location.href,
        hostname: window.location.hostname,
        port: window.location.port,
        protocol: window.location.protocol,
        userAgent: navigator.userAgent
      };
      
      console.table(info);
      return info;
    }
  };
  
  console.log("✅ Use the following commands:");
  console.log("  debug.testRoot() - Test both root endpoints");
  console.log("  debug.testChat('Your message') - Test chat endpoint");
  console.log("  debug.testRaw() - Test all possible API endpoints");
  console.log("  debug.testChatComponent('Your message') - Test the chat component directly");
  console.log("  debug.getNetworkInfo() - Get network configuration");
}

// Auto-load if directly included in a script tag
if (typeof window !== 'undefined') {
  window.loadApiDebugger = loadApiDebugger;
  console.log("API Debugger available. Run loadApiDebugger() to initialize.");
} 