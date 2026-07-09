#!/bin/bash
echo "🚀 TUNY Setup - By Gaïus Ouarahoun"
echo "======================================"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1/6] Checking Node.js...${NC}"
node --version || { echo "Install Node.js 18+"; exit 1; }
echo -e "${GREEN}✓ Node.js OK${NC}\n"

echo -e "${YELLOW}[2/6] Checking Python...${NC}"
python3 --version || { echo "Install Python 3.9+"; exit 1; }
echo -e "${GREEN}✓ Python OK${NC}\n"

echo -e "${YELLOW}[3/6] Creating .env...${NC}"
[ ! -f .env ] && cp .env.example .env
echo -e "${GREEN}✓ .env created${NC}\n"

echo -e "${YELLOW}[4/6] Installing frontend...${NC}"
cd tuny-build && npm install && cd ..
echo -e "${GREEN}✓ Frontend ready${NC}\n"

echo -e "${YELLOW}[5/6] Setting up Python...${NC}"
cd tuny && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ..
echo -e "${GREEN}✓ Backend ready${NC}\n"

echo -e "${YELLOW}[6/6] Creating directories...${NC}"
mkdir -p logs data ollama_models
echo -e "${GREEN}✓ Directories created${NC}\n"

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "${YELLOW}Run: npm run dev${NC}"
