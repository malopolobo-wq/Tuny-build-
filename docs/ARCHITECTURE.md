# TUNY-BUILD Architecture

## Overview

TUNY is a 3-tier system:

```
┌─────────────────┐
│  TUNY-BUILD UI  │  (React + Glassmorphism)
│  (Frontend)     │
└────────┬────────┘
         │ REST + WebSocket
         │
┌────────▼────────┐
│  TUNY API       │  (Flask/FastAPI)
│  (Backend)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
┌───▼──┐  ┌──▼───┐
│ LLMs │  │ Data │  (Ollama, Stable Diffusion, etc)
│      │  │      │
└──────┘  └──────┘
```

## Components

### TUNY (Backend)
- **Orchestrator** - Main AI engine
- **LLM Service** - Ollama integration
- **Multimodal** - Image, video, audio, speech
- **Code Analysis** - Static analysis
- **Compilation** - Multi-language compiler

### TUNY-BUILD (Frontend)
- **Chat Interface** - Talk to TUNY
- **Code Editor** - Monaco Editor
- **Preview Panel** - Live preview
- **Settings** - Configuration

### Enterprise Features
- **Collaboration** - Real-time with Yjs
- **Testing** - Auto-generated tests
- **Monitoring** - APM with OpenTelemetry
- **Sandboxing** - Docker + gVisor

## Data Flow

1. User writes prompt in TUNY-BUILD
2. Sent to TUNY API
3. TUNY analyzes with LLM
4. Generates plan + code
5. Returns to TUNY-BUILD for preview
6. User can compile, test, deploy

## Technologies

**Backend:** Python, Flask, Ollama, PyTorch
**Frontend:** React, TypeScript, Tailwind, Vite
**Real-time:** Yjs, WebSocket
**Database:** SQLite, PostgreSQL
**Monitoring:** OpenTelemetry, SigNoz
