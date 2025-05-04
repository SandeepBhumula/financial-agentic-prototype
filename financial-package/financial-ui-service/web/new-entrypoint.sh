#!/bin/sh
set -e

echo "=========================================="
echo "Financial Agent UI - Starting container"
echo "=========================================="

# Apply API proxy configuration if in Docker Compose network
if [ "$USE_API_PROXY" = "true" ] || [ "$DOCKER_COMPOSE" = "true" ]; then
    echo "Applying API proxy configuration for Docker Compose..."
    # Check if agents-api is resolvable
    if getent hosts agents-api; then
        echo "agents-api hostname is resolvable - using API proxy configuration"
        
        # Super simple approach: Create a minimal nginx config
        cat > /etc/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name localhost;

    # Enable gzip compression for better performance
    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_min_length 256;
    gzip_types
        application/javascript
        application/json
        application/x-javascript
        text/css
        text/javascript
        text/plain
        text/xml;

    # Status endpoint for health checking
    location /status {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'ok';
    }

    # Static assets with aggressive caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /usr/share/nginx/html;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        access_log off;
        try_files $uri =404;
    }

    # Handle React Router - No caching for index.html
    location = /index.html {
        root /usr/share/nginx/html;
        add_header Cache-Control "no-store, no-cache, must-revalidate";
        add_header Pragma "no-cache";
        expires 0;
    }

    # Handle React Router routes
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-store, no-cache, must-revalidate" always;
    }

    # API proxy configuration
    location /api/ {
        # Proxy to the agents-api service
        proxy_pass http://agents-api:8000/api/;
        
        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Origin, X-Requested-With, Content-Type, Accept, Authorization' always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Origin, X-Requested-With, Content-Type, Accept, Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }

    # Improved error handling
    error_page 404 /index.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOF
        
        echo "API proxy configuration applied successfully"
    else
        echo "Warning: agents-api hostname is not resolvable, using standalone mode"
    fi
else
    echo "Running in standalone mode - API will return mock responses"
fi

# Print diagnostic information
echo "==== NGINX CONFIGURATION ===="
cat /etc/nginx/conf.d/default.conf

# Check nginx configuration
echo "Checking Nginx configuration..."
nginx -t

# Start Nginx
echo "Starting Nginx server with daemon off"
exec nginx -g "daemon off;" 