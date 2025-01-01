# syntax=docker.io/docker/dockerfile:1

FROM node:22-alpine AS base

# Step 1. Build the application
FROM base AS builder

WORKDIR /app/client

# Install dependencies
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Copy source code and configuration
COPY src ./src
COPY public ./public
COPY next.config.mjs .
COPY tsconfig.json .

# Use build-time environment variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Build the Next.js application
RUN pnpm build

# Step 2. Prepare the production image
FROM base AS runner

WORKDIR /app/client

# Create a non-root user
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs
USER nextjs

# Copy built assets
COPY --from=builder /app/client/public ./public
COPY --from=builder /app/client/.next/standalone ./
COPY --from=builder /app/client/.next/static ./.next/static

# Use runtime environment variables
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Start the application
CMD ["node", "server.js"]
