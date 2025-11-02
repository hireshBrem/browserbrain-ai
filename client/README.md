# Browser Agent Context Enhancement - Client

> **Next.js frontend for browser agent context management**

This is the client application for the Browser Agent Context Enhancement project. It provides a web interface for interacting with browser automation agents, visualizing context and memory management, and real-time interaction with the browser automation API.

## 🎯 Overview

The client is a Next.js application that serves as the user interface for:
- Interacting with browser automation agents
- Visualizing context and memory management
- Real-time interaction with the browser automation API
- Monitoring agent performance and memory usage

## 🛠️ Tech Stack

- **Framework**: Next.js 16 (App Router)
- **React**: React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Build Tool**: Next.js built-in bundler

## 📦 Installation

### Prerequisites

- Node.js 20+
- npm, yarn, pnpm, or bun

### Setup

```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

## 🚀 Development

### Start Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

The client will be available at [http://localhost:3000](http://localhost:3000)

**Note**: Make sure the backend server is running on `http://localhost:4000` for the API to work properly.

### Build for Production

```bash
npm run build
# or
yarn build
# or
pnpm build
# or
bun build
```

### Start Production Server

```bash
npm start
# or
yarn start
# or
pnpm start
# or
bun start
```

## 🐳 Docker

The client can be run via Docker Compose (see root `docker-compose.yml`):

```bash
# From project root
docker-compose up
```

This will start both the client and server with hot reload enabled.

## 📁 Project Structure

```
client/
├── src/
│   └── app/                 # Next.js App Router directory
│       ├── page.tsx         # Main page component
│       ├── layout.tsx       # Root layout
│       ├── globals.css      # Global styles
│       └── favicon.ico      # Favicon
├── public/                  # Static assets
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── next.config.ts           # Next.js configuration
├── postcss.config.mjs       # PostCSS configuration
├── Dockerfile               # Docker container config
└── README.md                # This file
```

## 🔌 API Integration

The client communicates with the backend API running on `http://localhost:4000`. Current endpoints being used:

- `GET /` - Root endpoint (welcome message)
- `GET /health` - Health check endpoint

### Planned API Endpoints

- `POST /agent/execute` - Execute browser agent task
- `POST /memory/store` - Store agent experience in long-term memory
- `GET /memory/search` - Semantic search over agent history (RAG)
- `GET /cache/query` - Retrieve cached query trajectories
- `POST /cache/store` - Store successful query trajectory
- `GET /memory/history` - Retrieve agent interaction history

## 🎨 Features

### Current Implementation

- [x] Next.js 16 with App Router setup
- [x] TypeScript configuration
- [x] Tailwind CSS 4 styling
- [x] API health check integration
- [x] Error handling and loading states
- [x] Dark mode support
- [x] Responsive design

### Planned Features

- [ ] Browser agent task execution interface
- [ ] Memory visualization dashboard
- [ ] Context search and retrieval UI
- [ ] Real-time agent status monitoring
- [ ] Query trajectory visualization
- [ ] Memory history timeline
- [ ] Agent performance metrics

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the client directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:4000
```

### API URL Configuration

The API URL is currently hardcoded in `src/app/page.tsx`. Consider using environment variables for production deployments.

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API
- [React Documentation](https://react.dev) - learn about React
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) - learn about Tailwind CSS

## 🚀 Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out the [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT
