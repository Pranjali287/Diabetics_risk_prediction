#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")/.."

# Install dependencies
npm install

# Build the project (if applicable)
npm run build

# Transfer files to the server (replace with actual server details)
# scp -r ./dist/* user@yourserver:/path/to/deploy/

# Start the application (replace with actual start command)
# pm2 start src/main.js --name "my-project" 

echo "Deployment completed."