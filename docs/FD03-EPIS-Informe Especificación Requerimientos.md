# FD03 - Informe: Especificación de Requerimientos

Proyecto: Agente Revisor IA (Revisión automática y asistida de tesis)

---

## II. Visionamiento de la Empresa

### 1. Descripción del Problema

Los estudiantes y docentes enfrentan retrasos y variabilidad en la calidad de las revisiones de tesis. El proceso actual depende fuertemente de la disponibilidad del asesor, genera retroalimentación poco estructurada y demanda tiempo significativo. Existe la necesidad de un sistema que apoye el proceso de revisión, ofreciendo feedback inicial automático, control de versiones de documentos y una interfaz colaborativa para mejorar tiempos y calidad de las correcciones.

### 2. Objetivos de Negocios

- Reducir el tiempo promedio de devolución de revisiones preliminares en al menos 50% mediante automatización asistida.
- Incrementar la consistencia y trazabilidad de las observaciones realizadas sobre documentos académicos.
- Facilitar la interacción entre estudiantes y revisores mediante herramientas que centralicen documentos, comentarios y versiones.
- Proteger la confidencialidad y control de acceso de los trabajos académicos mediante autenticación y permisos.

### 3. Objetivos de Diseño

- Diseñar una interfaz clara y accesible para carga y visualización de documentos (PDF).
- Integrar un motor de IA para generar recomendaciones estructuradas (estructura, estilo, citas, coherencia) y resúmenes de observaciones.
- Permitir edición y comentarios colaborativos por parte de los revisores humanos sobre las sugerencias automáticas.
- Implementar un backend escalable y modular que permita sustituir o actualizar el motor de IA y servicios asociados.

### 4. Alcance del proyecto

Incluye:
- Módulo de autenticación y gestión de usuarios (estudiantes, revisores, administradores).
- Carga, extracción y almacenamiento de documentos PDF con versionamiento.
- Servicio de análisis automático que genera un informe preliminar usando modelos de lenguaje (integración Gemini).
- Interfaz de chat y panel de revisión para visualizar observaciones, comentar y aceptar/descartar sugerencias.
- Persistencia en Supabase y APIs REST para gestión de recursos.

No incluye (fuera de alcance inicial):
- Evaluación académica formal (calificación automática final).
- Integración con repositorios institucionales externos (solo Supabase como backend inicial).

### 5. Viabilidad del Sistema

Técnica: Alta — la arquitectura propuesta usa tecnologías modernas: FastAPI (backend), Next.js (frontend), Supabase (DB/auth), y modelos LLM (servicio gemini_service). Existe código base y servicios para procesamiento PDF y orquestación.
Económica: Moderada — costes asociados al uso de la API de modelos de lenguaje, almacenamiento y despliegue. Se recomienda plan piloto para validar costos.
Legal y privacidad: Requiere políticas de tratamiento de datos y consentimiento explícito para almacenar trabajos académicos. Implementar cifrado en tránsito y buenas prácticas en almacenamiento.

### 6. Información obtenida del Levantamiento de Información

- Roles: estudiantes (suben tesis), revisores (profesores), administradores.
- Flujo típico: el estudiante solicita revisión, sube PDF, el revisor revisa y devuelve observaciones. Latencias prolongadas en la coordinación.
- Necesidades destacadas: reportes estructurados, control de versiones, historial de comentarios, seguimiento de estado de revisión.
- Restricciones: confidencialidad, formatos mayormente en PDF, variabilidad en longitud y formato de tesis.

## III. Análisis de Procesos

### a) Diagrama del Proceso Actual – Diagrama de actividades (descripción)

Flujo actual (manual):
1. Estudiante comunica al asesor la necesidad de revisión.
2. Estudiante envía documento por correo o almacenamiento compartido.
3. Asesor descarga y revisa localmente (anota PDF o documento Word).
4. Asesor comparte observaciones por correo o reunión; genera múltiples versiones sin control centralizado.
5. Estudiante integra comentarios y reenvía; proceso iterativo con tiempos largos.

Problemas identificados: falta de control de versiones, dispersión de feedback, tiempos de espera largos, ausencia de trazabilidad estructurada.

### b) Diagrama del Proceso Propuesto – Diagrama de actividades Inicial (descripción)

Flujo propuesto automatizado/colaborativo:
1. Estudiante se registra e inicia sesión en la plataforma.
2. Estudiante sube la versión del documento (PDF) en el panel de tesis.
3. El sistema extrae texto (servicio PDF) y almacena la versión en Supabase.
4. Se solicita revisión automática: el servicio de IA (gemini_service) analiza el documento y genera un informe preliminar con secciones (estructura, gramática, referencias, coherencia, sugerencias de mejora).
5. Revisor recibe notificación y accede al panel de revisión donde puede: aceptar/editar/añadir comentarios sobre las sugerencias automáticas.
6. Generación de reporte final y versionamiento de documento; histórico disponible para ambas partes.

Beneficios: respuesta rápida inicial, trazabilidad, control de versiones, colaboración integrada.

## IV. Especificación de Requerimientos de Software

### a) Cuadro de Requerimientos funcionales Inicial

- RF-01: Registro de usuarios (Estudiante, Revisor, Admin). Prioridad: Alta. Criterio de aceptación: un usuario puede registrarse y autenticarse mediante correo y contraseña; roles asignables.
- RF-02: Carga de documentos PDF. Prioridad: Alta. Criterio: el sistema acepta PDF hasta tamaño configurable (ej. 50 MB) y confirma extracción básica de texto.
- RF-03: Generación de revisión automática. Prioridad: Alta. Criterio: tras la subida, se genera un informe preliminar que contiene observaciones y se guarda como borrador.
- RF-04: Panel de revisión colaborativa. Prioridad: Alta. Criterio: revisor y autor pueden ver comentarios, marcar ítems como resueltos.
- RF-05: Historial de versiones. Prioridad: Media. Criterio: cada subida crea un registro de versión con metadatos.
- RF-06: Descarga de informe final en PDF. Prioridad: Media. Criterio: generación y descarga de un PDF con las observaciones consolidadas.

### b) Cuadro de Requerimientos No funcionales

- RNF-01: Seguridad — Autenticación y autorización basada en roles. Prioridad: Alta. Criterio: acceso restringido por rol; endpoints protegidos.
- RNF-02: Rendimiento — Tiempo de respuesta para análisis automático < 30s para documentos < 10,000 palabras (sujeto a carga). Prioridad: Media.
- RNF-03: Disponibilidad — SLA objetivo 99% (horas de operación estándar). Prioridad: Media.
- RNF-04: Escalabilidad — Arquitectura modular para escalar servicios de IA independientemente. Prioridad: Media.
- RNF-05: Privacidad — Cifrado en tránsito (TLS) y manejo confidencial de documentos. Prioridad: Alta.
- RNF-06: Mantenibilidad — Código documentado y pruebas unitarias. Prioridad: Media.

### c) Cuadro de Requerimientos funcionales Final

Tras el análisis y priorización:
- RFF-01: Autenticación con Supabase y roles (Estudiante, Revisor, Admin). Aceptación: login/logout, recuperación de contraseña.
- RFF-02: Subida y preprocesado de PDF con extracción de texto completa y segmentación por capítulos.
- RFF-03: Revisión automática por motor LLM con reportes estructurados (secciones: estructura, contenido, estilo, referencias, lista de mejoras). Aceptación: informe con métricas y 10 ítems accionables mínimo para tesis > 5k palabras.
- RFF-04: Interfaz de revisión que permita editar, comentar, aceptar/rechazar ítems y versionar cambios.
- RFF-05: Logs y auditoría de acciones sobre documentos y revisiones.
- RFF-06: API REST bien documentada para operaciones clave (subida, solicitud de revisión, consulta de informes).

### d) Reglas de Negocio

- RN-01: Solo usuarios autenticados pueden subir documentos.
- RN-02: El revisor humano puede anular o editar cualquier sugerencia automática.
- RN-03: Los documentos no se publican públicamente sin consentimiento explícito del autor.
- RN-04: Cada versión de documento queda registrada con usuario, fecha y resumen de cambios.
- RN-05: Los informes automáticos deben indicar claramente que son sugerencias generadas por IA.

## V. Fase de Desarrollo

### 1. Perfiles de Usuario

- Estudiante (autor): Subir documentos, ver informes, aplicar sugerencias, descargar reportes.
- Revisor (profesor): Acceder a documentos asignados, añadir comentarios, aceptar/rechazar sugerencias, generar informe final.
- Administrador: Gestionar usuarios, parámetros del sistema, visualizar métricas y logs.
- Sistema (Servicios): Procesamiento de PDF, orquestación de peticiones a modelos LLM, almacenamiento.

### 2. Modelo Conceptual

#### a) Diagrama de Paquetes (descripción)

Paquetes principales:
- Frontend: componentes React/Next.js (PDFViewer, ThesisReviewPanel, ChatWindow, UploadZone).
- API: routers (auth, chat, documents, thesis_review) expuestos por FastAPI (main.py).
- Core: lógica de negocio y configuraciones (auth.py, config.py).
- Servicios: gemini_service (IA), pdf_service (extracción y preprocesamiento), supabase_service (persistencia y auth).
- Database: supabase_repository y esquema SQL.

#### b) Diagrama de Casos de Uso (descripción)

Actores: Estudiante, Revisor, Administrador.
Casos de uso clave:
- Registrarse / Iniciar sesión.
- Subir tesis y crear versión.
- Solicitar revisión automática.
- Revisar y comentar (humano).
- Generar y descargar informe final.

#### c) Escenarios de Caso de Uso (narrativa)

Escenario 1 — Subir tesis y solicitar revisión automática:
1. Estudiante ingresa a la plataforma y sube el PDF.
2. Sistema procesa el PDF y extrae texto.
3. Estudiante solicita revisión automática.
4. Servicio IA genera informe preliminar; sistema notifica al revisor.

Escenario 2 — Revisión y validación humana:
1. Revisor accede al panel y revisa el informe preliminar.
2. Añade comentarios, modifica sugerencias y guarda cambios.
3. Revisor marca los ítems resueltos y publica informe final.

Escenario 3 — Iteración autor-revisor:
1. Estudiante revisa las observaciones y sube nueva versión.
2. Sistema versiona el documento y registra la iteración en el histórico.

### 3. Modelo Lógico

#### a) Análisis de Objetos

Objetos principales:
- User {id, nombre, correo, rol, fecha_creacion}
- Thesis {id, titulo, autor_id, versiones: [Document], fecha_creacion, estado}
- Document {id, thesis_id, version, archivo_url, texto_extraido, metadatos}
- Review {id, document_id, autor_revisor_id, tipo(IA|HUMANO), contenido, estado}
- Comment {id, review_id, usuario_id, texto, fecha}
- Report {id, thesis_id, resumen, fecha_generacion, formato_pdf}

Relaciones: User 1..* Thesis; Thesis 1..* Document; Document 0..* Review; Review 0..* Comment.

#### b) Diagrama de Actividades con objetos (descripción)

Actividad: "Generar revisión automática"
- Actor: Estudiante solicita revisión.
- Objetos: Document -> texto_extraido -> Petición a gemini_service -> Review(IA) -> Report.
- Flujo: subida -> extracción -> petición IA -> recepción informe -> almacenamiento -> notificación.

#### c) Diagrama de Secuencia (descripción)

Caso: Revisión automática
1. Usuario (Estudiante) -> Frontend: subirDocumento()
2. Frontend -> API: POST /documents
3. API -> pdf_service: extraerTexto(documento)
4. API -> supabase_repository: guardarDocumento(metadata)
5. API -> gemini_service: solicitarAnalisis(texto_segmentado)
6. gemini_service -> API: devolverInforme(estructuraJSON)
7. API -> supabase_repository: guardarReview(IA)
8. API -> Frontend: notificarDisponibilidad(informe)

#### d) Diagrama de Clases (descripción)

Clases principales (resumen):
- User: atributos {id, name, email, role}
- Thesis: {id, title, author}
- Document: {id, thesisId, version, url, extractedText}
- Review: {id, documentId, reviewerId, type, content, status}
- PDFService: métodos {extract_text(file)}
- GeminiService: métodos {analyze_text(text, options)}
- SupabaseRepository: métodos {save_document(), get_document(), save_review()}

Relaciones: Document pertenece a Thesis; Review referencia Document y User.

## CONCLUSIONES

- El sistema propuesto reduce fricción en el proceso de revisión mediante una capa de revisión automática que entrega feedback estructurado.
- La arquitectura modular (frontend, API, servicios, DB) facilita la evolución del producto y la sustitución del motor de IA.
- Los riesgos principales son costos por uso de modelos LLM y la gestión de privacidad de documentos; ambas necesidades requieren políticas y controles técnicos.

## RECOMENDACIONES

- Implementar un piloto con un conjunto limitado de usuarios para evaluar la calidad del feedback automático y calibrar costos.
- Generar diagramas UML (PlantUML) a partir de las descripciones para validar con stakeholders (diagramas de casos de uso, secuencia y clases).
- Definir límites y políticas de retención de documentos y consentimiento explícito al subir tesis.
- Añadir pruebas automáticas para los servicios críticos (pdf_service, gemini_service mocks) y pruebas de integración con Supabase.
- Planificar métricas clave (tiempo medio de entrega, cantidad de iteraciones por tesis, tasa de aceptación de sugerencias IA).

---

Documento generado en base al alcance y código existente en el repositorio (backend con servicios gemini_service, pdf_service y persistencia en Supabase; frontend con paneles para visualización y revisión).
