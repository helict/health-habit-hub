FROM node:22-alpine

# Use production node environment by default.
ENV NODE_ENV=production


WORKDIR /usr/src/app

# Install dependencies first (leverages Docker layer cache)
COPY --chown=node:node package*.json ./
RUN npm ci --omit=dev --verbose



# Copy the rest of the source files into the image.
COPY --chown=node:node . .

# Run the application as a non-root user.
USER node

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["npm", "run", "start"]
