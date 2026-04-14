1. Frontend: Next.js (La Cara del Proyecto)
El frontend será el único punto de contacto con el estudiante. Su trabajo es ser rápido, interactivo y mostrar la información de forma limpia.

¿Qué hará?

Gestión de Interfaz (UI): Mostrará un panel dividido. A la izquierda, un visor para leer el PDF de la tesis; a la derecha, la interfaz de chat con el agente de IA.

Gestión de Estado: Recordará si el usuario está subiendo un archivo, si la IA está "pensando" o si hubo un error.

Streaming en tiempo real: Usará el Vercel AI SDK para recibir las respuestas de Gemini palabra por palabra, dando la sensación de que la IA está escribiendo en vivo.

¿Cómo se dividirá internamente?

app/ o pages/: Aquí irán tus rutas web (ej. /dashboard, /login, /chat).

components/: Tus bloques de lego visuales.

ChatWindow.tsx: La caja de mensajes.

PDFViewer.tsx: El componente para mostrar el documento.

UploadZone.tsx: El botón de arrastrar y soltar para subir la tesis.

lib/ o services/: Archivos con las funciones que hacen las llamadas fetch o axios a tu backend de FastAPI.

2. Backend: FastAPI + Uvicorn (El Cerebro Controlador)
Este es el núcleo de tu monolito. Uvicorn es el servidor web que mantendrá FastAPI corriendo. Tu backend nunca renderiza HTML; solo recibe peticiones del frontend, procesa datos y devuelve respuestas en formato JSON.

¿Qué hará?

Recepción de Archivos: Recibirá el PDF que envía el frontend y extraerá todo el texto (puedes usar librerías de Python como PyMuPDF o pdfplumber).

Orquestación de la IA (RAG): Tomará el texto del PDF, lo dividirá en partes pequeñas, pedirá los vectores y los guardará.

Seguridad y Reglas: Se asegurará de que un usuario no pueda consultar o chatear con la tesis de otro usuario.

¿Cómo se dividirá internamente?

main.py: El punto de entrada donde inicias la app y configuras los CORS (vital para que Next.js pueda hablar con FastAPI sin errores de seguridad).

routers/: Para mantener el código limpio, separarás las rutas.

documents.py: Rutas tipo POST /api/upload para subir PDFs.

chat.py: Rutas tipo POST /api/chat para enviar preguntas a la IA.

services/: La lógica pesada.

gemini_service.py: El código que se conecta a la API de Google.

pdf_service.py: El código que extrae y limpia el texto de las tesis.

database/: Archivos para conectarse a Supabase desde Python usando su SDK o SQLAlchemy.

3. Base de Datos: Supabase (La Memoria a Largo Plazo)
Supabase es fundamental porque te da PostgreSQL con la extensión pgvector ya instalada, lo que lo hace perfecto para aplicaciones de IA.

¿Qué hará?

Autenticación (Opcional pero recomendado): Puedes usar Supabase Auth para manejar los registros y logins de usuarios fácilmente.

Almacenamiento Relacional: Guardará quién es dueño de qué tesis.

Almacenamiento Vectorial: Guardará los "fragmentos matemáticos" de las tesis para que la IA pueda buscarlos rápido.

¿Qué tablas vas a necesitar crear?

users: ID, email, fecha de registro.

documents: ID del documento, ID del usuario (dueño), nombre del archivo (ej. tesis_final_v3.pdf), fecha de subida.

document_chunks: Aquí ocurre la magia. Tendrá: ID del fragmento, ID del documento al que pertenece, content (el párrafo en texto real) y embedding (una columna tipo vector donde se guarda la representación matemática de ese párrafo).

4. Inteligencia Artificial: API de Gemini 1.5 (El Motor de Razonamiento)
Gemini 1.5 es excepcional para este proyecto por su enorme ventana de contexto. Hará dos trabajos distintos a través de tu backend.

¿Qué hará?

Trabajo 1: Crear Embeddings (Vectores). Cuando el backend extrae el texto de la tesis, se lo envía al modelo text-embedding-004 de Gemini. Este modelo no responde preguntas; solo devuelve una enorme lista de números (el vector) que representa el significado de ese texto. Ese vector es el que guardas en Supabase.

Trabajo 2: Asesorar (Generación de Texto). Usarás gemini-1.5-pro o gemini-1.5-flash. Cuando el alumno hace una pregunta, tu backend le enviará a Gemini:

La instrucción del sistema ("Eres un asesor de tesis estricto pero útil...").

Los fragmentos de la tesis recuperados de Supabase.

La pregunta del alumno.
Gemini leerá todo eso y devolverá la respuesta redactada.

El Flujo de Trabajo Completo (Paso a Paso)
Para que lo veas en acción, así funcionará el sistema cuando lo termines:

Sube la tesis: El alumno entra a tu web en Next.js y sube su PDF.

Procesamiento: Next.js envía el PDF a FastAPI. FastAPI usa Python para leer el texto y lo corta en 500 párrafos.

Vectorización: FastAPI envía esos 500 párrafos a la API de embeddings de Gemini. Gemini devuelve 500 vectores.

Almacenamiento: FastAPI guarda los párrafos y sus vectores en Supabase.

La Pregunta: El alumno escribe en Next.js: "¿Mi marco metodológico está bien planteado?".

La Búsqueda: Next.js envía la pregunta a FastAPI. FastAPI convierte esa pregunta en un vector (usando Gemini) y le dice a Supabase: "Busca los 5 párrafos de la tesis de este usuario que matemáticamente se parezcan más a la pregunta".

El Razonamiento: FastAPI toma esos 5 párrafos específicos (que casualmente son del capítulo de metodología) y se los manda a Gemini 1.5 junto con la pregunta.

La Respuesta: Gemini 1.5 analiza los párrafos, redacta una crítica constructiva y la envía de vuelta a FastAPI, quien se la pasa a Next.js para que el alumno la lea en pantalla.