# TUNY Setup Guide

## Prerequisites

- Node.js 18+
- Python 3.9+
- Docker (optional but recommended)
- GPU (recommended for Ollama)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/malopolobo-wq/Tuny-build-.git
cd Tuny-build-
```

### 2. Automated Setup

```bash
bash scripts/setup-dev.sh
```

### 3. Configure Environment

Edit `.env` with your settings.

### 4. Start Ollama (if not using Docker)

```bash
ollama serve
```

In another terminal:

```bash
ollama pull llama2:70b
ollama pull mistral
```

### 5. Start Development

```bash
npm run dev
```

TUNY-BUILD will be at `http://localhost:5173`

## Docker Setup

```bash
docker-compose up -d
```

Then visit `http://localhost:5173`

## Troubleshooting

### Ollama not running

```bash
ollama serve
```

### Port already in use

Change ports in `.env` or `docker-compose.yml`

### No GPU support

Install appropriate drivers or use CPU (slower)
