# Azure OpenAI Chat App

## Setup Instructions

### 1. Backend (Python)
1. Open terminal and go to `backend/`
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn openai
   ```
3. Open `main.py` and replace:
   - `YOUR_AZURE_OPENAI_KEY`
   - `YOUR_AZURE_OPENAI_ENDPOINT`
   - `YOUR_DEPLOYMENT_NAME`
4. Run backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 2. Frontend (React)
1. Open terminal and go to `frontend/`
2. Create vite app if not already:
   ```bash
   npm create vite@latest .
   npm install axios
   ```
3. Replace `src/App.jsx` with provided file
4. Run frontend:
   ```bash
   npm run dev
   ```

### 3. Usage
- Open browser at http://localhost:5173
- Type a message
- See Azure OpenAI reply!
