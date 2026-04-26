<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *Agente de IA para Revisión y Asesoría de Tesis***

Curso: *Patrones de Software*

Docente: *Patrick José Cuadros Quiroga*

Integrantes:

***Ayala Ramos, Carlos Daniel (2022074266)***
 
***Loyola Vilca, Renzo Fernando (2021072615)***
 
***Vargas Candia, Hashira Belén (2022075480)***

**Tacna – Perú**

***2026***


<<<<<<< HEAD
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1.0|MPV|ELV|ARV|07/04/2026|Versión Original|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# INDICE GENERAL

- Antecedentes ............................................................ 1
- Planteamiento del Problema .............................................. 4
  - Problema
  - Justificación
  - Alcance
- Objetivos ............................................................... 6
- Marco Teórico
- Desarrollo de la Solución .............................................. 9
- Análisis de Factibilidad (técnico, económica, operativa, social, legal, ambiental)
- Tecnología de Desarrollo
- Metodología de implementación (Documento de VISION, SRS, SAD)
- Cronograma ............................................................ 11
- Presupuesto ........................................................... 12
- Conclusiones .......................................................... 13
- Recomendaciones ....................................................... 14
- Bibliografía .......................................................... 15
- Anexos ............................................................... 16
  - Anexo 01 Informe de Factibilidad
  - Anexo 02 Documento de Visión
  - Anexo 03 Documento SRS
  - Anexo 04 Documento SAD
  - Anexo 05 Manuales y otros documentos

---

## Contenido (Informe Final)
## Antecedentes

En las instituciones académicas la revisión de trabajos de titulación suele ser un proceso manual, fragmentado y con alta dependencia en la disponibilidad del asesor. Esto provoca retrasos, pérdida de trazabilidad en las versiones y retroalimentación heterogénea. El presente proyecto nace como respuesta a la necesidad de apoyar y optimizar este proceso mediante la integración de herramientas de extracción y análisis de documentos (PDF) y un motor de lenguaje para generar retroalimentación preliminar que facilite la labor del revisor humano.

Este informe consolida los resultados del desarrollo del sistema, recoge la justificación técnica y organizacional, y presenta el plan de cierre, cronograma y presupuesto estimado.

## Planteamiento del Problema

### a. Problema

Los procesos de revisión de tesis actualmente tienen las siguientes deficiencias:
- Retrasos significativos en la devolución de observaciones.
- Retroalimentación no estructurada y difícil de rastrear.
- Ausencia de control centralizado de versiones.
- Alta carga de trabajo manual para los asesores.

### b. Justificación

Una plataforma que automatice tareas repetitivas (extracción de texto, análisis preliminar y generación de sugerencias) y centralice la colaboración entre estudiante y revisor permitirá:
- Reducir tiempos de respuesta y número de iteraciones.
- Estandarizar la calidad de las observaciones.
- Mantener un histórico de versiones y acciones para auditoría.
- Liberar tiempo de los asesores para actividades de mayor valor académico.

### c. Alcance

Incluye:
- Autenticación y gestión de roles (Estudiante, Revisor, Administrador).
- Carga, extracción y almacenamiento de documentos PDF con versionamiento.
- Servicio de revisión automática (integración con modelo LLM — gemini_service) que genera un informe preliminar estructurado.
- Panel colaborativo para revisar, comentar y aceptar/rechazar sugerencias.
- Persistencia en Supabase y APIs REST para integraciones.

Fuera del alcance (fase inicial):
- Calificación automática final de trabajos.
- Integraciones con sistemas institucionales externos no especificadas.

## Objetivos

- Objetivo general: Implementar una plataforma que mejore la eficiencia y calidad del proceso de revisión de tesis mediante la automatización asistida y herramientas de colaboración.

- Objetivos específicos:
  - Desarrollar la API y servicios de backend para manejo de documentos y orquestación de análisis IA.
  - Implementar interfaz web con visualización de PDFs, panel de revisión y chat colaborativo.
  - Integrar un motor de LLM para generar informes preliminares con observaciones estructuradas.
  - Garantizar seguridad, versionado y trazabilidad de las revisiones.

## Marco Teórico

La solución se apoya en tecnologías y conceptos probados:
- Modelos de Lenguaje (LLMs): para análisis de coherencia, estilo y estructura, y para generar sugerencias accionables.
- Procesamiento de Lenguaje Natural (NLP): técnicas para detección de errores gramaticales, extracción de entidades y resumen automático.
- Extracción de texto de PDFs: para transformar documentos a texto plano y segmentarlos por capítulos/secciones.
- Arquitectura cliente-servidor y servicios desacoplados: para escalar componentes (servicio IA independiente, servicio de extracción, repositorio).
- Control de acceso basado en roles y buenas prácticas de privacidad y almacenamiento.

Para detalles de requisitos y diagramas, ver el SRS y los diagramas UML en la carpeta `docs/` (FD03 y `docs/diagrams`).

## Desarrollo de la Solución

### a) Análisis de Factibilidad

- Técnica: Alta. El repositorio ya contiene un backend en FastAPI, servicios de extracción de PDF y módulos para integrar modelos LLM (`gemini_service`). La arquitectura propuesta es modular y compatible con despliegue en entornos en la nube.

- Económica: Moderada. Costes principales asociados al consumo de APIs de modelos de lenguaje y al hosting (base de datos, almacenamiento de archivos). Se recomienda un piloto para ajustar presupuesto según uso real.

- Operativa: Alta viabilidad operativa si se capacita a usuarios clave (asesores y personal de TI). Requiere definir políticas de uso y respaldo de datos.

- Social: Positiva — reduce fricciones en la interacción estudiante-asesor, mejora la percepción de rapidez en el proceso académico.

- Legal: Requiere cumplimiento de normativas de protección de datos y consentimiento explícito para almacenar trabajos académicos. Implementar cifrado en tránsito (TLS) y políticas de retención.

- Ambiental: Bajo impacto directo; uso de recursos en la nube con huella energética limitada respecto al beneficio operativo.

### b) Tecnología de Desarrollo

- Frontend: Next.js (React), componentes para visualización de PDF y panel de revisión.
- Backend: Python + FastAPI, routers para `auth`, `documents`, `thesis_review`, `chat`.
- Base de datos y autenticación: Supabase (Postgres), repositorio `supabase_repository.py`.
- Servicios: `pdf_service` (extracción y preprocesado), `gemini_service` (análisis LLM), `supabase_auth_service`.
- Infraestructura: despliegue en cloud (opciones: Vercel/Netlify para frontend, servidor containerizado o serverless para backend), uso de almacenamiento de objetos para PDFs.
- Herramientas de desarrollo: Git/GitHub, PlantUML para diagramas, pytest para pruebas, linters y CI según alcance.

### c) Metodología de implementación (Documento de VISION, SRS, SAD)

Se propone un enfoque iterativo (Scrum ligero):
- Documento de VISIÓN: define alcance, actores y valor del producto (ya documentado en FD02/FD03).
- SRS (Software Requirements Specification): consolidación de requisitos funcionales y no funcionales (FD03 sirve como base SRS).
- SAD (Software Architecture Document): diagramas de paquetes, clases y secuencias (carpeta `docs/diagrams`).

Fases de implementación:
1. Planificación y refinamiento de requisitos (visión/SRS).
2. Implementación del backend y servicios de almacenamiento/versionado.
3. Integración del `pdf_service` y pipeline de preprocesado.
4. Integración y pruebas de `gemini_service` con casos representativos.
5. Desarrollo del frontend y UX del panel de revisión.
6. Pruebas de integración, despliegue y piloto con usuarios reales.

## Cronograma (ejemplo)

Plan estimado de 12 semanas (3 meses):
- Semanas 1-2: Requisitos finales y diseño arquitectónico (SRS, SAD).
- Semanas 3-4: Implementación backend inicial y autenticación.
- Semanas 5-6: Servicio de extracción PDF y persistencia de versiones.
- Semanas 7-8: Integración LLM y generación de informes preliminares.
- Semanas 9-10: Frontend y panel de revisión; pruebas de usabilidad.
- Semana 11: Despliegue piloto y correcciones.
- Semana 12: Evaluación del piloto y plan de escalamiento.

(El cronograma debe ajustarse según recursos y resultados del piloto.)

## Presupuesto (estimación)

Categorías y estimaciones aproximadas (valores en USD):
- Desarrollo (3 personas: backend, frontend, devops) por 3 meses: 30,000 - 45,000.
- Infraestructura y hosting (mensual): 50 - 300.
- APIs LLM (variará según uso): 200 - 2,000 por mes en piloto/producción temprana.
- Licencias, herramientas y contingencias: 1,000 - 3,000.
- Imprevistos (10% del total): variable.

Nota: estos valores son referenciales; se requiere cotización con proveedores y estimación de uso real para afinar presupuesto.

## Conclusiones

El proyecto "Agente Revisor IA" presenta una solución práctica y viable para mejorar la eficiencia y calidad del proceso de revisión de tesis. La existencia de un prototipo y módulos base en el repositorio reduce el riesgo técnico. Los principales retos son la gestión de costos asociados al uso de modelos LLM y el cumplimiento de políticas de privacidad.

Con una implementación iterativa y un piloto controlado se pueden validar los supuestos y ajustar el alcance antes de un despliegue a mayor escala.

## Recomendaciones

- Ejecutar un piloto con un conjunto limitado de usuarios y medir métricas clave (tiempo medio de revisión, número de iteraciones, satisfacción del revisor).
- Definir y publicar una política de privacidad y retención de documentos.
- Implementar métricas y monitoreo del consumo de APIs LLM para controlar costes.
- Generar pruebas automáticas para `pdf_service` y `gemini_service` (mocks) para asegurar calidad.
- Documentar procesos de despliegue y un plan de escalabilidad.

---

Documentos de referencia: ver [docs/FD03-EPIS-Informe Especificación Requerimientos.md](docs/FD03-EPIS-Informe%20Especificaci%C3%B3n%20Requerimientos.md) y el directorio [docs/diagrams](docs/diagrams/) para diagramas UML.

## Metodología de implementación

[Describir metodología de desarrollo (iterativa, ágil, SCRUM), artefactos entregables: Documento de Visión, SRS, SAD.]

## Cronograma

[Incluir cronograma por fases y actividades principales.]

## Presupuesto

[Desglose de costos estimados por rubro y total.]

## Conclusiones

[Conclusiones generales del trabajo realizado, resultados esperados y limitaciones.]

## Recomendaciones

[Sugerencias para la continuidad, mejoras y consideraciones futuras.]

## Bibliografía

[Listado de referencias bibliográficas y recursos consultados.]

## Anexos

- Anexo 01 Informe de Factibilidad
- Anexo 02 Documento de Visión
- Anexo 03 Documento SRS
- Anexo 04 Documento SAD
- Anexo 05 Manuales y otros documentos


Documento creado siguiendo la carátula y estructura solicitadas. Rellena las secciones con el contenido del proyecto cuando lo desees.
