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

**  
**
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|07/04/2026|Versión Original|












**Sistema *Agente de IA para Revisión y Asesoría de Tesis***

**Documento de Visión**

**Versión *{1.0}***
**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|10/10/2020|Versión Original|


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


**INDICE GENERAL**
#

- [1. Introducción](#1-introducción)
  - [1.1 Propósito](#11-propósito)
  - [1.2 Alcance](#12-alcance)
  - [1.3 Definiciones, Siglas y Abreviaturas](#13-definiciones-siglas-y-abreviaturas)
  - [1.4 Referencias](#14-referencias)
  - [1.5 Visión General](#15-visión-general)
- [2. Posicionamiento](#2-posicionamiento)
  - [2.1 Oportunidad de negocio](#21-oportunidad-de-negocio)
  - [2.2 Definición del problema](#22-definición-del-problema)
- [3. Descripción de los interesados y usuarios](#3-descripción-de-los-interesados-y-usuarios)
  - [3.1 Resumen de los interesados](#31-resumen-de-los-interesados)
  - [3.2 Resumen de los usuarios](#32-resumen-de-los-usuarios)
  - [3.3 Entorno de usuario](#33-entorno-de-usuario)
  - [3.4 Perfiles de los interesados](#34-perfiles-de-los-interesados)
  - [3.5 Perfiles de los usuarios](#35-perfiles-de-los-usuarios)
  - [3.6 Necesidades de los interesados y usuarios](#36-necesidades-de-los-interesados-y-usuarios)
- [4. Vista General del Producto](#4-vista-general-del-producto)
  - [4.1 Perspectiva del producto](#41-perspectiva-del-producto)
  - [4.2 Resumen de capacidades](#42-resumen-de-capacidades)
  - [4.3 Suposiciones y dependencias](#43-suposiciones-y-dependencias)
  - [4.4 Costos y precios](#44-costos-y-precios)
  - [4.5 Licenciamiento e instalación](#45-licenciamiento-e-instalación)
- [5. Características del producto](#5-características-del-producto)
- [6. Restricciones](#6-restricciones)
- [7. Rangos de calidad](#7-rangos-de-calidad)
- [8. Precedencia y Prioridad](#8-precedencia-y-prioridad)
- [9. Otros requerimientos del producto](#9-otros-requerimientos-del-producto)
  - [9.1 Estándares legales](#91-estándares-legales)
  - [9.2 Estándares de comunicación](#92-estándares-de-comunicación)
  - [9.3 Estándares de cumplimiento de la plataforma](#93-estándares-de-cumplimiento-de-la-plataforma)
  - [9.4 Estándares de calidad y seguridad](#94-estándares-de-calidad-y-seguridad)
- [Conclusiones](#conclusiones)
- [Recomendaciones](#recomendaciones)
- [Bibliografía](#bibliografía)
- [Webgrafía](#webgrafía)
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
**Informe de Visión**
 
## 1. Introducción
 
El presente documento describe el sistema denominado Agente de IA para Revisión y Asesoría de Tesis. Este sistema tiene como finalidad apoyar a los estudiantes en el proceso de elaboración de sus tesis, facilitando la revisión, retroalimentación y orientación en cada etapa del desarrollo del trabajo.
La propuesta busca mejorar la calidad de los trabajos académicos mediante el uso de tecnologías de inteligencia artificial, permitiendo brindar sugerencias, detectar posibles errores y orientar al usuario de manera más rápida y eficiente. De esta manera, se pretende ofrecer una herramienta que complemente el proceso de asesoría tradicional y ayude a optimizar el tiempo tanto de estudiantes como de asesores.

 
### 1.1 Propósito
 
El propósito de este documento es definir, de manera clara y estructurada, la visión del sistema Agente de IA para Revisor y Asesoría de Tesis, estableciendo el contexto del problema, los involucrados, las necesidades del negocio y las características principales del producto. Este documento sirve como guía base para el equipo de desarrollo y los interesados, alineando expectativas y delimitando el alcance del proyecto.
 
### 1.2 Alcance
 
El sistema no reemplaza la función del asesor humano, sino que actúa como una herramienta de apoyo complementaria para estudiantes de pregrado y posgrado.
 
### 1.3 Definiciones, Siglas y Abreviaturas
 
| Término | Definición |
| :- | :- |
| IA | Inteligencia Artificial: tecnología que permite a los sistemas aprender, razonar y tomar decisiones. |
| PLN | Procesamiento de Lenguaje Natural: rama de la IA para análisis y comprensión del lenguaje humano. |
| IEEE | Institute of Electrical and Electronics Engineers: organismo que define estándares técnicos. |
| LLM | Large Language Model: modelo de lenguaje de gran escala utilizado en sistemas de IA generativa. |
| API | Application Programming Interface: interfaz de programación para integración entre servicios. |
| RAG | Retrieval-Augmented Generation: técnica que combina recuperación de información con generación de texto. |
 
### 1.4 Referencias
 
 
### 1.5 Visión General

El presente documento está organizado en nueve secciones principales. La sección 1 presenta la introducción, alcance y definiciones clave. La sección 2 describe el posicionamiento del producto, incluyendo la oportunidad de negocio y la definición del problema. La sección 3 caracteriza a los interesados y usuarios del sistema. La sección 4 proporciona una vista general del producto con sus capacidades, suposiciones y costos. Las secciones 5 al 9 detallan las características del producto, restricciones, rangos de calidad, prioridades y otros requerimientos complementarios.
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 2. Posicionamiento
 
### 2.1 Oportunidad de negocio
 
En el contexto universitario, uno de los principales desafíos que enfrentan los estudiantes es la elaboración de su tesis para obtener el grado o título profesional. Este proceso suele ser largo y complejo, ya que requiere cumplir con normas académicas, metodológicas y de formato, además de constantes revisiones por parte de un asesor.
Sin embargo, muchas veces existe una limitación en la disponibilidad de los asesores, quienes deben atender a varios estudiantes al mismo tiempo. Esto puede generar retrasos en la retroalimentación, poca orientación en momentos clave y, en algunos casos, desmotivación en los estudiantes.
Frente a esta situación, el desarrollo de un Agente de IA para Revisión y Asesoría de Tesis representa una oportunidad importante, ya que permitiría brindar apoyo constante, accesible en cualquier momento, con retroalimentación rápida y personalizada. Además, considerando el crecimiento de las tecnologías educativas, este tipo de solución tiene potencial para implementarse en diferentes instituciones y mejorar significativamente el proceso de elaboración de tesis.

 
### 2.2 Definición del problema
 
El problema principal que se busca resolver es la falta de retroalimentación oportuna y personalizada durante el desarrollo de tesis, así como el desconocimiento de normas académicas por parte de los estudiantes, lo que genera errores frecuentes.
Este problema afecta principalmente a estudiantes que se encuentran elaborando su tesis, así como a los asesores que deben revisar múltiples trabajos al mismo tiempo.
Como consecuencia, se produce un aumento en el tiempo necesario para culminar la tesis, errores repetitivos en los documentos, frustración en los estudiantes y una sobrecarga de trabajo en los asesores.
Una posible solución es el desarrollo de un sistema basado en inteligencia artificial que permita revisar automáticamente los documentos de tesis, identificar errores de redacción, estructura y citación, y brindar sugerencias en tiempo real, además de ofrecer un espacio de consulta interactivo para orientar al estudiante durante todo el proceso.

 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 3. Descripción de los interesados y usuarios
 
En esta sección se identifican las personas que están involucradas en el uso y desarrollo del sistema, así como sus necesidades y funciones dentro del proyecto.
 
### 3.1 Resumen de los interesados
 
| Nombre | Descripción | Responsabilidad |
| :- | :- | :- |
| Estudiantes de UPT | Alumnos de pregrado y posgrado en proceso de elaboración de tesis. | Usuarios principales del sistema; cargan documentos y consultan retroalimentación. |
| Docentes Asesores | Profesores responsables de guiar la elaboración de tesis. | Monitorean el progreso de sus tesistas a través del panel del sistema. |
| Coordinadores Académicos | Encargados de velar por el cumplimiento del reglamento de tesis. | Definen los estándares y criterios de evaluación integrados al sistema. |
| Equipo de Desarrollo | Grupo responsable del diseño e implementación del sistema. | Diseñan, desarrollan y mantienen el sistema. |
| Administración UPT | Autoridades institucionales de la universidad. | Aprueban e impulsan la implementación del sistema en la institución. |
 
### 3.2 Resumen de los usuarios
 
| Nombre | Descripción | Responsabilidad | Interesado |
| :- | :- | :- | :- |
| Tesista | Estudiante que elabora su tesis. | Carga documentos, revisa sugerencias y consulta al agente. | Estudiantes de UPT |
| Asesor | Docente que guía el proceso. | Supervisa avances y configura parámetros de revisión. | Docentes Asesores |
| Administrador del Sistema | Personal técnico a cargo. | Gestiona usuarios, plantillas y configuración general. | Equipo de Desarrollo / UPT |
 
### 3.3 Entorno de usuario
 
 
### 3.4 Perfiles de los interesados
 
 
### 3.5 Perfiles de los usuarios

 
### 3.6 Necesidades de los interesados y usuarios
 
| Necesidad | Prioridad | Interesados | Solución Actual | Solución Propuesta |
| :- | :-: | :- | :- | :- |
| Retroalimentación oportuna en la revisión de tesis | Alta | Tesistas, Asesores | Revisión manual con demoras de días o semanas. | Revisión automática en minutos mediante IA. |
| Verificación de normas APA/IEEE | Alta | Tesistas | Revisión manual por el asesor. | Módulo automático de verificación de citas y referencias. |
| Asesoría disponible fuera de horario académico | Alta | Tesistas | Correo o mensajería con respuesta tardía. | Chatbot con IA disponible 24/7. |
| Seguimiento del avance por capítulos | Media | Asesores, Coordinadores | Reuniones periódicas. | Panel de seguimiento integrado en el sistema. |
| Detección de similitudes y plagio | Alta | Coordinadores, Asesores | Herramientas externas de pago. | Módulo de detección de similitudes integrado. |
| Acceso centralizado desde cualquier dispositivo | Media | Todos los usuarios | No existe solución unificada. | Aplicación web responsiva accesible desde cualquier navegador. |
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 4. Vista General del Producto
 
### 4.1 Perspectiva del producto
 
El Agente de IA para Revisión y Asesoría de Tesis es un sistema web independiente diseñado para apoyar el proceso de elaboración de trabajos de investigación. Este sistema no busca reemplazar otras herramientas académicas existentes, sino complementarlas, brindando una ayuda adicional en la revisión y mejora de los documentos.
 
Desde el punto de vista técnico, el sistema estará conformado por los siguientes módulos principales:
 
- **Motor de revisión documental:** encargado de analizar archivos, evaluando aspectos como la estructura, coherencia, redacción y uso correcto de citas mediante inteligencia artificial..
- **Agente conversacional:** un chat interactivo que permitirá al usuario realizar consultas sobre metodología, normas académicas y desarrollo de la tesis.
- **Módulo de detección de similitudes:** permitirá identificar posibles coincidencias con otras fuentes, ayudando a prevenir el plagio.
- **Panel de seguimiento:** mostrará el avance del trabajo por capítulos, facilitando el control tanto para el estudiante como para el asesor.
- **Sistema de autenticación y gestión de usuarios:** controlará el acceso al sistema según el tipo de usuario (tesista, asesor o administrador).
 
El sistema será implementado en la nube, lo que permitirá que esté disponible en todo momento, además de garantizar un buen rendimiento, escalabilidad y seguridad en el manejo de la información.
 
### 4.2 Resumen de capacidades
 
 
### 4.3 Suposiciones y dependencias
 
**Suposiciones:**
 
- Los usuarios (tesistas y asesores) cuentan con acceso a internet de manera regular.
- La institución aprobará y promoverá el uso de la herramienta como apoyo complementario al asesor.
- Los documentos de tesis se presentarán en formatos estándar (PDF o DOCX).
- Los modelos de IA utilizados mantendrán una precisión aceptable para el contexto académico universitario peruano.
 
**Dependencias:**
 
- Disponibilidad de APIs de modelos de lenguaje de gran escala (LLM) de proveedores externos.
- Infraestructura de nube (AWS, GCP o Azure) para el despliegue del sistema.
- Acceso a bases de datos académicas para el módulo de detección de similitudes.
- Lineamientos y reglamentos oficiales de tesis de la Universidad Privada de Tacna.
- Soporte institucional para la integración con el sistema académico existente de la UPT.
 
### 4.4 Costos y precios
 
 
### 4.5 Licenciamiento e instalación
 
El sistema será desarrollado bajo una licencia académica de uso interno para la Universidad Privada de Tacna durante la fase de prototipo. Para su implementación productiva se contemplan las siguientes consideraciones:
 
- La instalación se realizará en entornos cloud mediante contenedores Docker, facilitando la escalabilidad.
- El acceso al sistema requerirá credenciales institucionales proporcionadas por la UPT.
- Las APIs externas (LLM, detección de similitudes) se integrarán mediante claves de acceso administradas por el equipo técnico.
- El código fuente del proyecto será gestionado en un repositorio privado bajo control de versiones Git.
- En su fase de expansión, el sistema podrá licenciarse a otras instituciones educativas bajo un esquema SaaS.
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 5. Características del producto
 
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 6. Restricciones
 
- El sistema soportará únicamente idioma español en su versión inicial, con posibilidad de expansión al inglés.
- La precisión del análisis de similitudes depende de la cobertura de las bases de datos académicas integradas.
- El sistema no tendrá acceso a documentos confidenciales del sistema académico institucional sin previa integración oficial.
- El presupuesto de desarrollo está limitado al alcance de un proyecto académico universitario de pregrado.
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 7. Rangos de calidad
 
| Atributo de Calidad | Descripción | Métrica Objetivo |
| :- | :- | :- |
| Rendimiento | El sistema debe procesar y analizar un documento de tesis promedio (80 páginas) en tiempo aceptable. | Tiempo de respuesta máximo: 3 minutos por documento. |
| Disponibilidad | El sistema debe estar disponible de forma continua para los usuarios. | Uptime mínimo del 99% mensual. |
| Usabilidad | La interfaz debe ser intuitiva y no requerir capacitación especializada. | Tasa de adopción mayor al 80% tras primera sesión de uso. |
| Seguridad | Los documentos de los tesistas deben estar protegidos y ser confidenciales. | Cifrado TLS en tránsito y AES-256 en reposo. Autenticación con JWT. |
| Precisión del Análisis | La retroalimentación generada debe ser relevante y útil para el tesista. | Satisfacción del usuario mayor al 80% en encuestas de retroalimentación. |
| Escalabilidad | El sistema debe soportar un incremento en el número de usuarios sin degradación del servicio. | Soporte para al menos 500 usuarios concurrentes en versión productiva. |
| Mantenibilidad | El sistema debe permitir actualizaciones y mejoras sin interrupciones mayores. | Arquitectura modular con cobertura de pruebas unitarias mayor al 70%. |
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 8. Precedencia y Prioridad
 
| N° | Característica | Prioridad | Fase | Justificación |
| :-: | :- | :-: | :-: | :- |
| 1 | Carga y procesamiento de documentos | Crítica | Fase 1 | Base del sistema; sin ella no opera ninguna otra función. |
| 2 | Revisión automatizada con IA | Crítica | Fase 1 | Funcionalidad central del producto. |
| 3 | Generación de reportes de retroalimentación | Alta | Fase 1 | Permite al tesista actuar sobre las observaciones. |
| 4 | Gestión de usuarios y roles | Alta | Fase 1 | Necesaria para seguridad y acceso diferenciado. |
| 5 | Módulo de chat conversacional | Alta | Fase 2 | Añade asesoría 24/7; clave para el valor diferencial. |
| 6 | Detección de similitudes | Media | Fase 2 | Importante para integridad académica. |
| 7 | Panel de seguimiento de progreso | Media | Fase 2 | Complementa la experiencia del asesor. |
| 8 | Historial de versiones del documento | Baja | Fase 3 | Agrega valor pero no es crítico para el MVP. |
 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## 9. Otros requerimientos del producto
 
### 9.1 Estándares legales
 
El sistema debe cumplir con el marco legal peruano e internacional aplicable al tratamiento de datos personales y propiedad intelectual:
 
- **Ley N° 29733 - Ley de Protección de Datos Personales del Perú** y su reglamento (D.S. N° 003-2013-JUS): el sistema garantizará el tratamiento adecuado de los datos personales de los usuarios, incluyendo el consentimiento informado para el procesamiento de sus documentos académicos.
- **Ley N° 28132 - Ley de Derechos de Autor del Perú:** los documentos de tesis cargados al sistema serán tratados con confidencialidad y los derechos de autoría pertenecerán a los estudiantes. El sistema no compartirá ni publicará los documentos sin autorización expresa.
 
### 9.2 Estándares de comunicación
 
 
### 9.3 Estándares de cumplimiento de la plataforma
 

### 9.4 Estándares de calidad y seguridad
 

 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## Conclusiones
 
- El Agente de IA para Revisión y Asesoría de Tesis surge como una alternativa útil para ayudar a resolver el problema de la falta de retroalimentación rápida durante el desarrollo de una tesis. Mediante el uso de inteligencia artificial, el sistema puede apoyar a los estudiantes brindando sugerencias y observaciones en menor tiempo, lo que puede mejorar su proceso de aprendizaje.
- En este documento se ha podido definir de manera clara qué es lo que se quiere desarrollar, quiénes van a usar el sistema y cuáles son sus principales funciones. Además, se han considerado aspectos importantes como las restricciones y la calidad del sistema, lo que permitirá tener una mejor organización durante su desarrollo.
- Es importante mencionar que este sistema no busca reemplazar al asesor, sino más bien servir como un apoyo. De esta forma, el asesor puede enfocarse en aspectos más importantes del trabajo, mientras que el sistema ayuda con revisiones más básicas o repetitivas.

 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## Recomendaciones
 
- Se recomienda involucrar activamente a docentes asesores y estudiantes tesistas en las etapas de validación del prototipo, para asegurar que la retroalimentación generada por el sistema sea relevante y útil en el contexto académico de la UPT.
- Es fundamental establecer mecanismos claros de consentimiento informado para el tratamiento de los documentos de tesis, garantizando el cumplimiento de la Ley de Protección de Datos Personales del Perú.
- Se recomienda iniciar con un piloto controlado en una sola escuela profesional antes de la implementación institucional masiva, a fin de identificar ajustes necesarios en el flujo de revisión y la calidad de la retroalimentación.
- El equipo de desarrollo debe mantenerse actualizado respecto a los avances en modelos de lenguaje de gran escala, considerando la rápida evolución del campo de la inteligencia artificial generativa.

 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## Bibliografía
 
- Russell, S. & Norvig, P. (2021). Artificial Intelligence: A Modern Approach (4.ª ed.). Pearson Education.
- American Psychological Association. (2020). Publication Manual of the American Psychological Association (7.ª ed.). APA.
- IEEE. (2016). IEEE Editorial Style Manual. Institute of Electrical and Electronics Engineers.
- Gamma, E., Helm, R., Johnson, R. & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.
- Pressman, R. S. & Maxim, B. R. (2020). Ingeniería del Software: Un enfoque práctico (8.ª ed.). McGraw-Hill.

 
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
 
## Webgrafía
 
- World Wide Web Consortium (W3C). (2018). Web Content Accessibility Guidelines (WCAG) 2.1. Recuperado de https://www.w3.org/TR/WCAG21/ 
- Ministerio de Justicia del Perú. (2013). Ley N° 29733 - Ley de Protección de Datos Personales. Recuperado de https://www.minjus.gob.pe/privacidad/ 
- LangChain. (2024). LangChain Documentation - Building LLM Applications. Recuperado de https://python.langchain.com/docs/ 
