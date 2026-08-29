FROM node:22-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with locked versions
RUN npm ci

# Copy application
COPY . .

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev"]
