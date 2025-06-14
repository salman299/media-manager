# Media Manager Frontend

A React-based frontend application for managing and displaying media content, built with modern web technologies.

## Architecture Overview

### Tech Stack
- React 19.1.0 with TypeScript
- Redux Toolkit 2.8.2 for state management
- TailwindCSS 3.4.17 for styling
- Modern browser support with browserslist configuration

## Features
- Responsive media grid display
- Advanced search and filtering capabilities
- Real-time search suggestions
- Error handling and loading states
- Modern, responsive design
- Optimized image loading and caching

## Setup Instructions

### Prerequisites
- Node.js 22 (managed via nvm)
- Backend API running (see backend repository)

### Environment Setup

#### Node.js Setup with nvm
1. Install nvm (if not already installed):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

2. Add nvm to your shell configuration:
```bash
# Add to ~/.zshrc or ~/.bashrc
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

3. Install and use Node.js 22:
```bash
nvm install 22
nvm use 22
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env  # Create your .env file from example
# Edit .env with your API endpoint and other settings
```

3. Start the development server:
```bash
npm start
```

### Production Setup
To build the application for production:
```bash
npm run build
# Serve the build directory using your preferred web server
```

## Development Considerations

### State Management
- Redux Toolkit for global state management
- Optimized selectors and reducers
- Efficient state updates and caching

### Styling
- TailwindCSS for utility-first styling
- Responsive design patterns
- Modern UI components

### Performance
- Code splitting and lazy loading
- Optimized image loading
- Efficient state updates
- Browser caching strategies

## License
MIT

## Author
Ali Salman
