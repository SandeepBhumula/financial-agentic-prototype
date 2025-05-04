# Build stage
FROM node:16.20.0-alpine as build

# Set environment variables for better Node.js performance and stability
ENV NODE_ENV=production
ENV PATH /app/node_modules/.bin:$PATH
ENV CI=false
ENV GENERATE_SOURCEMAP=true

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY web/package*.json ./

# Install dependencies with clean npm install
RUN echo "Installing dependencies..." && \
    npm install --legacy-peer-deps && \
    npm install react-scripts@5.0.1 --save && \
    echo "Dependencies installed successfully."

# Verify react-scripts is installed
RUN if [ ! -f "node_modules/.bin/react-scripts" ]; then \
      echo "ERROR: react-scripts not installed properly"; \
      exit 1; \
    fi

# Copy source code
COPY web/ ./

# Create a .env file with production configurations
RUN echo "REACT_APP_API_URL=/api" > .env.production.local && \
    echo "REACT_APP_VERSION=$(date '+%Y%m%d-%H%M')" >> .env.production.local

# Build the application
RUN SKIP_PREFLIGHT_CHECK=true npm run build

# Production stage
FROM nginx:stable-alpine

# Install necessary utilities
RUN apk add --no-cache curl bash tzdata

# Create web app directory 
WORKDIR /usr/share/nginx/html

# Remove default nginx static assets
RUN rm -rf ./*

# Copy build files from build stage
COPY --from=build /app/build ./

# Copy nginx configuration 
COPY web/nginx.conf /etc/nginx/conf.d/default.conf

# Environment variables
ENV USE_API_PROXY=true
ENV DOCKER_COMPOSE=true

# Expose port
EXPOSE 80

# Command to run nginx
CMD ["nginx", "-g", "daemon off;"] 