# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your frontend code
COPY . .

# Build the frontend (for production)
RUN npm run build

# Expose the port (default for Next.js is 3000)
EXPOSE 3000

# Start the app
CMD ["npm", "start"]

