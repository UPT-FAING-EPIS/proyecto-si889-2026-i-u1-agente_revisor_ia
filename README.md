# Asesor IA de Tesis (Next.js + FastAPI + Supabase + Gemini)

Aplicacion web para estudiantes que permite:

1. Registrarse e iniciar sesion.
2. Subir una tesis en PDF.
3. Procesar el documento con RAG (chunks + embeddings).
4. Chatear con un asesor IA que responde usando el contexto real de la tesis.

## Arquitectura

### Frontend (Next.js)

- Rutas App Router: login, registro y dashboard.
- Panel dividido: visor PDF + chat IA.
- Streaming de respuesta con Vercel AI SDK (`useCompletion`).
- Estado de sesion y token usando contexto React.

Ubicacion principal:

- `frontend/app/`
- `frontend/components/`
- `frontend/lib/`

### Backend (FastAPI)

- API REST y streaming en texto.
- Endpoints de auth, upload y chat.
- Extraccion de PDF con `pypdf`.
- Gemini para embeddings y generacion de texto.
- Supabase como almacenamiento relacional/vectorial.

Ubicacion principal:

- `backend/app/main.py`
- `backend/app/routers/`
- `backend/app/services/`
- `backend/app/database/`

## Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/upload`
- `GET /api/documents`
- `POST /api/chat` (streaming)

## Esquema SQL (Supabase)

Ejecuta el script:

- `backend/sql/schema.sql`

Este script crea:

1. Tabla `documents`.
2. Tabla `document_chunks` con columna `embedding vector(768)`.
3. Funcion `match_document_chunks(...)` para busqueda semantica.

## Configuracion de entorno

### Backend

1. Copia `backend/.env.example` en tu archivo de variables.
2. Define valores reales para Gemini y Supabase.

Variables clave:

- `GEMINI_API_KEY` (o `API_GEMINI` por compatibilidad)
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (obligatoria para el backend con RLS)
- `SUPABASE_PUBLISHABLE_KEY` (opcional para clientes frontend)
- `CORS_ORIGINS` (por defecto `http://localhost:3000`)

### Frontend

1. Copia `frontend/.env.local.example` a `frontend/.env.local`.
2. Define `NEXT_PUBLIC_BACKEND_URL` (por defecto `http://localhost:8000`).

### Despliegue en GitHub Pages (frontend estatico)

El frontend se puede exportar a estatico y publicar en GitHub Pages. El backend FastAPI y Supabase
deben estar desplegados por separado (ej. Render, Railway, Fly, VPS). Para que funcione:

1. Configura en el backend `CORS_ORIGINS` con la URL final de GitHub Pages.
2. En GitHub Actions define:
   - `NEXT_PUBLIC_BACKEND_URL` con la URL publica del backend.
   - (opcional) `NEXT_PUBLIC_BASE_PATH` con el nombre del repositorio si no coincide con `GITHUB_REPOSITORY`.

Los secretos de Supabase (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, etc.) permanecen en el backend,
no deben exponerse en GitHub Pages.

## Ejecucion local

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre `http://localhost:3000`.

## Flujo funcional

1. Usuario crea cuenta o inicia sesion.
2. Sube tesis PDF desde el dashboard.
3. Backend extrae texto, lo trocea, genera embeddings y guarda en Supabase.
4. Usuario pregunta en chat.
5. Backend vectoriza la pregunta, recupera chunks relevantes y consulta Gemini.
6. La respuesta llega en streaming al frontend.

## Notas de seguridad y buenas practicas

1. El backend valida `Authorization: Bearer` en rutas protegidas.
2. Cada consulta de chat verifica que el documento pertenezca al usuario autenticado.
3. Se recomienda habilitar RLS en Supabase para reforzar aislamiento por usuario.
