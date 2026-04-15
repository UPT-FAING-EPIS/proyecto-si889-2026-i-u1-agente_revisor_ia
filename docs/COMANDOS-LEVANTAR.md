python: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend: npm run dev

# Comandos para levantar el proyecto

Este documento te permite verificar y levantar backend (FastAPI) y frontend (Next.js).

## 1) Verificar si ya estan corriendo

Ejecuta estos comandos desde la raiz del repositorio:

```bash
curl -sS http://localhost:8000/health
curl -I http://localhost:3000
```

Si el backend responde `{"status":"ok"}` y el frontend responde `HTTP/1.1 200`, ya estan arriba.

## 1.1) Configuracion recomendada para evitar "Failed to fetch"

El frontend ahora usa un proxy interno de Next.js (`/backend`) para reenviar peticiones a FastAPI y evitar problemas de CORS/mixed-content.

En `frontend/.env.local` usa:

```bash
NEXT_PUBLIC_BACKEND_URL=/backend
BACKEND_INTERNAL_URL=http://127.0.0.1:8000
```

## 2) Levantar Backend (FastAPI)

Abre una terminal y ejecuta:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si aun no tienes archivo local de entorno en backend:

```bash
cp .env.example .env
```

Inicia el servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3) Levantar Frontend (Next.js)

Abre otra terminal y ejecuta:

```bash
cd frontend
npm install
```

Si aun no tienes archivo local de entorno en frontend:

```bash
cp .env.local.example .env.local
```

Si ya existia `frontend/.env.local`, verifica que use el proxy interno como en la seccion 1.1.

Inicia el servidor:

```bash
npm run dev
```

## 4) URLs de trabajo

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger FastAPI: http://localhost:8000/docs

## 5) Verificar flujo completo

1. Registra o inicia sesion en el frontend.
2. Sube un PDF desde el dashboard.
3. Haz una pregunta en el chat.
4. Verifica que el backend procese la consulta y responda streaming.

## 6) Si un puerto esta ocupado

### Ver procesos

```bash
lsof -iTCP:3000 -sTCP:LISTEN -P
lsof -iTCP:8000 -sTCP:LISTEN -P
```

### Terminar proceso por PID

```bash
kill -9 <PID>
```

## 7) Reinicio rapido

Cuando ya instalaste dependencias previamente:

### Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

## 8) Procedimiento rapido cuando sale "Failed to fetch"

1. Deten ambos servidores (`Ctrl + C` en cada terminal).
2. Verifica `frontend/.env.local` con proxy interno:

```bash
NEXT_PUBLIC_BACKEND_URL=/backend
BACKEND_INTERNAL_URL=http://127.0.0.1:8000
```

3. Levanta backend:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Levanta frontend:

```bash
cd frontend
npm run dev
```

5. Abre la web y prueba en este orden:
	- Crear cuenta
	- Iniciar sesion

## 9) Probar acceso a modelos Gemini (aislado)

Si el chat responde con fallback y no con Gemini, ejecuta la prueba de modelos:

```bash
cd backend
source .venv/bin/activate
python scripts/probe_gemini_models.py --update-env --env-file ../.env
```

Que hace este script:

1. Prueba varios modelos de chat y embeddings.
2. Detecta modelos disponibles por `list_models`.
3. Intenta una llamada real a cada modelo.
4. Guarda en `../.env` los modelos funcionales detectados (`GEMINI_CHAT_MODEL` y `GEMINI_EMBEDDING_MODEL`).

Luego reinicia backend y frontend.
