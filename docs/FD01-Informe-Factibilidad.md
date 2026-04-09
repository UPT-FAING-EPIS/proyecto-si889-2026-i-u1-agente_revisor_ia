<center>

![./media/logo-upt.png](./media/logo-upt.png)

[cite_start]**UNIVERSIDAD PRIVADA DE TACNA** [cite: 1]

[cite_start]**FACULTAD DE INGENIERÍA** [cite: 1]

[cite_start]**Escuela Profesional de Ingeniería de Sistemas** [cite: 1]

[cite_start]**Proyecto: "Agente de IA para Revisión y Asesoría de Tesis"** [cite: 1]

[cite_start]Curso: Patrones de Software [cite: 1]

Docente: Ing. [cite_start]Patrick Cuadros Quiroga [cite: 1]

[cite_start]Integrantes: [cite: 1]

[cite_start]**Ayala Ramos, Carlos Daniel (2022074266)** [cite: 1]
[cite_start]**Loyola Vilca, Renzo Fernando (2021072615)** [cite: 1]
[cite_start]**Vargas Candia, Hashira Belén (2022075480)** [cite: 1]

[cite_start]**Tacna – Perú** [cite: 1]

[cite_start]**2026** [cite: 1]

** **
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

[cite_start]Sistema Agente de IA para Revisión y Asesoría de Tesis [cite: 1]

[cite_start]Informe de Factibilidad [cite: 1]

[cite_start]Versión 1.0 [cite: 1]

[cite_start]|CONTROL DE VERSIONES|||||| [cite: 1]
| :-: | :- | :- | :- | :- | :- |
[cite_start]|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo| [cite: 1]
[cite_start]|1.0|-|-|-|10/04/2025|Versión Original| [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# [cite_start]**ÍNDICE GENERAL** [cite: 1]

[1. [cite_start]Descripción del Proyecto](#_Toc52661346) [cite: 1]

[cite_start][1.2 Duración del proyecto](#_Toc52661346) [cite: 1]

[cite_start][1.3 Descripción](#_Toc52661346) [cite: 1]

[cite_start][1.4 Objetivos](#_Toc52661346) [cite: 1]

[2. [cite_start]Riesgos](#_Toc52661347) [cite: 1]

[3. [cite_start]Análisis de la Situación actual](#_Toc52661348) [cite: 1]

[4. [cite_start]Estudio de Factibilidad](#_Toc52661349) [cite: 1]

[cite_start][4.1 Factibilidad Técnica](#_Toc52661350) [cite: 1]

[cite_start][4.2 Factibilidad Económica](#_Toc52661351) [cite: 1]

[cite_start][4.3 Factibilidad Operativa](#_Toc52661352) [cite: 1]

[cite_start][4.4 Factibilidad Legal](#_Toc52661353) [cite: 1]

[cite_start][4.5 Factibilidad Ambiental](#_Toc52661355) [cite: 1]

[5. [cite_start]Análisis Financiero](#_Toc52661356) [cite: 1]

[6. [cite_start]Conclusiones](#_Toc52661357) [cite: 1]


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

[cite_start]**<u>Informe de Factibilidad</u>** [cite: 1]

1. [cite_start]<span id="_Toc52661346" class="anchor"></span>**Descripción del Proyecto** [cite: 1]

    1.1. [cite_start]Nombre del proyecto [cite: 1]

    Sistema Agente de IA para Revisión y Asesoría de Tesis. [cite: 1]

    1.2. Duración del proyecto [cite: 1]

    | FASES | DURACIÓN | [cite: 1]
    | :--- | :--- |
    | INICIO | DEL 31/03/2026 AL 04/04/2026 | [cite: 1]
    | ELABORACIÓN | DEL 05/04/2026 AL 05/05/2026 | [cite: 1]
    | CONSTRUCCIÓN | DEL 06/05/2026 AL 31/05/2026 | [cite: 1]
    | TRANSICIÓN | DEL 01/06/2026 AL 18/06/2026 | [cite: 1]

    1.3. Descripción [cite: 1]

    El sistema tiene como propósito modernizar y agilizar el proceso de revisión de tesis universitarias. [cite: 1] Actualmente, los tesistas sufren largas esperas para recibir retroalimentación, y los asesores están saturados de trabajo. [cite: 1] Con este nuevo sistema web, se busca brindar una plataforma impulsada por Inteligencia Artificial (mediante LLMs como Gemini u OpenAI) que permita pre-evaluar la redacción, el formato (APA, IEEE, etc.), la coherencia metodológica y detectar posibles plagios, sirviendo como un "co-asesor" disponible 24/7. [cite: 1]

    1.4. Objetivos [cite: 1]

    1.4.1 Objetivo general [cite: 1]
    Desarrollar e implementar un Agente de IA web que optimice los tiempos de revisión de tesis, mejorando la calidad académica de los documentos y reduciendo la carga operativa de los asesores humanos. [cite: 1]

    1.4.2 Objetivos Específicos [cite: 1]
    * Implementar un módulo de procesamiento de lenguaje natural (NLP) para analizar estructura, coherencia y formato de documentos académicos (PDF/Word). [cite: 1]
    * Permitir el registro y autenticación segura de usuarios (estudiantes y asesores). [cite: 1]
    * Generar reportes automáticos detallados con sugerencias de mejora y correcciones ortotipográficas. [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

2. [cite_start]<span id="_Toc52661347" class="anchor"></span>**Riesgos** [cite: 1]

    [cite_start]Los riesgos identificados en el proyecto se pueden clasificar en tres categorías de acuerdo con su frecuencia y efectos potenciales: [cite: 1]

    | Frecuencia de Riesgo | Valores | [cite: 1]
    | :--- | :--- |
    | Bajo | 1 | [cite: 1]
    | Medio | 2 | [cite: 1]
    | Alto | 3 | [cite: 1]

    | Riesgo | Valor | Efecto | [cite: 1]
    | :--- | :--- | :--- |
    | Privacidad de datos: Filtración de investigaciones inéditas al procesarlas a través de APIs de terceros | 3 | Catastrófico | [cite: 1]
    | Alucinaciones de la IA: Que el agente sugiera bibliografía falsa o correcciones metodológicas incorrectas | 2 | Serio | [cite: 1]
    | Costos de API: Incremento de costos operativos si los usuarios suben documentos demasiado pesados de forma constante | 1 | Moderado | [cite: 1]
    | Rechazo institucional: Que las universidades o asesores consideren el uso de la IA como una falta a la ética académica | 2 | Serio | [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. [cite_start]<span id="_Toc52661348" class="anchor"></span>**Análisis de la Situación actual** [cite: 1]

    3.1. [cite_start]Planteamiento del problema [cite: 1]

    El modelo actual de asesoría de tesis es un cuello de botella en las universidades. [cite: 1] Los asesores humanos tienen múltiples alumnos y poco tiempo, lo que genera retrasos de semanas para una simple revisión de formato o redacción. [cite: 1] Esto causa frustración, prolonga el tiempo de titulación y disminuye la calidad de las investigaciones por la falta de iteraciones rápidas. [cite: 1]

    3.2. Consideraciones de hardware y software [cite: 1]

    **Hardware:** [cite: 1]
    * **Computadora de desarrollo:** Procesador Intel Core i7 (o superior), 16 GB de RAM, SSD de 256 GB (mínimo) y monitor con resolución mínima de 1920x1080 píxeles. [cite: 1]
    * **Servidor VPS para despliegue:** vCPU de 4 núcleos (mínimo), 8 GB de RAM (mínimo), 100 GB SSD y sistema operativo Linux (Debian 12.10 o similar). [cite: 1]

    **Software:** [cite: 1]
    * Sistema Operativo: Windows 10 PRO. [cite: 1]
    * IDE: Visual Studio Code o similar. [cite: 1]
    * Servidor Web: Apache HTTP Server. [cite: 1]
    * Base de Datos: PostgreSQL. [cite: 1]
    * Lenguaje de Programación: PHP (puro, sin framework). [cite: 1]
    * Otras herramientas: JasperReports (opcional), Git y Consola SSH. [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. [cite_start]<span id="_Toc52661349" class="anchor"></span>**Estudio de Factibilidad** [cite: 1]

    [cite_start]El Estudio de Factibilidad del proyecto tiene como objetivo evaluar la viabilidad del proyecto desde varias perspectivas: técnica, económica, operativa y organizacional. [cite: 1]

    4.1. <span id="_Toc52661350" class="anchor"></span>Factibilidad Técnica [cite: 1]

    El estudio de factibilidad técnica evalúa si los recursos tecnológicos disponibles permiten el desarrollo e implementación del sistema de manera eficiente y segura. [cite: 1] El desarrollo se realizará localmente con equipos adecuados para tareas de codificación y pruebas. [cite: 1] Se utilizará PHP puro y PostgreSQL, tecnologías compatibles con entornos de producción web. [cite: 1] El despliegue final se contempla en una VPS con servidor Apache. [cite: 1] La seguridad incluirá validación de datos, cifrado de contraseñas y protección contra inyecciones SQL. [cite: 1] El uso de Git permitirá el control de versiones y la integridad del código. [cite: 1]

    4.2. <span id="_Toc52661351" class="anchor"></span>Factibilidad Económica [cite: 1]

    4.2.1. Costos Generales [cite: 1]
    Incluye insumos como papel bond, tinta, lapiceros y accesorios, con un total estimado de S/. 195.00. [cite: 1]

    4.2.2. Costos operativos durante el desarrollo [cite: 1]
    Incluye servicios de luz (S/. 240.00) e Internet (S/. 210.00) por 3 meses, sumando S/. 450.00. [cite: 1]

    4.2.3. Costos del ambiente [cite: 1]
    Incluye dominio web (S/. 55.00), VPS por 3 meses (S/. 180.00) y certificado SSL (S/. 80.00), totalizando S/. 315.00. [cite: 1]

    4.2.4. Costos de personal [cite: 1]
    Contempla 4 roles (Backend, Frontend, UI/UX y Analista) con 220 horas estimadas cada uno a una tarifa de S/. 2.27 por hora, resultando en S/. 2,000.00 en total. [cite: 1]

    4.2.5. Costos totales del desarrollo del sistema [cite: 1]
    El costo total del proyecto asciende a S/. 2,960.00. [cite: 1]

    4.3. <span id="_Toc52661352" class="anchor"></span>Factibilidad Operativa [cite: 1]

    El sistema busca automatizar el acceso a la información y brindar seguimiento individualizado. [cite: 1] Se diseñará para ser intuitivo y accesible desde cualquier dispositivo con internet. [cite: 1] El personal será capacitado en el registro de información y generación de reportes para garantizar una correcta adopción. [cite: 1]

    4.4. <span id="_Toc52661353" class="anchor"></span>Factibilidad Legal [cite: 1]

    El proyecto debe cumplir con la Ley de Protección de Datos Personales. [cite: 1] Se establecerán políticas de privacidad y términos de uso, requiriendo el consentimiento explícito de los usuarios. [cite: 1] El uso de tecnologías de código abierto evita conflictos de licencias privativas. [cite: 1]

    4.5. <span id="_Toc52661355" class="anchor"></span>Factibilidad Ambiental [cite: 1]

    El proyecto reduce el uso de papel al digitalizar documentación. [cite: 1] Optimiza la energía mediante el uso de servidores eficientes y promueve la movilidad sostenible al permitir gestiones 100% en línea. [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

5. [cite_start]<span id="_Toc52661356" class="anchor"></span>**Análisis Financiero** [cite: 1]

    5.1. [cite_start]Justificación de la Inversión [cite: 1]
    Se espera aumentar el número de usuarios al facilitar el acceso a la información y reducir la carga operativa mediante la digitalización. [cite: 1]

    5.1.2. Criterios de Inversión [cite: 1]
    Dada la naturaleza del proyecto, se realiza una evaluación cualitativa con una inversión estimada de S/. 855.00 (costos de ambiente y operativos), riesgo financiero bajo y beneficio estratégico alto. [cite: 1]

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

6. [cite_start]<span id="_Toc52661357" class="anchor"></span>**Conclusiones** [cite: 1]

    * [cite_start]El proyecto es viable técnica, económica, operativa y legalmente. [cite: 1]
    * [cite_start]Resuelve ineficiencias en procesos manuales y falta de transparencia. [cite: 1]
    * [cite_start]Los riesgos son manejables con atención a la seguridad y control de costos. [cite: 1]
    * [cite_start]Beneficia al medio ambiente al reducir papel y desplazamientos físicos. [cite: 1]
