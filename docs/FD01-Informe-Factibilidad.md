![Logo UPT](./media/logo-upt.png)

# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERÍA
### Escuela Profesional de Ingeniería de Sistemas

**Proyecto:** "Agente de IA para Revisión y Asesoría de Tesis"

**Curso:** Patrones de Software  
**Docente:** Ing. Patrick Cuadros Quiroga

**Integrantes:**
- **Ayala Ramos, Carlos Daniel (2022074266)**
- **Loyola Vilca, Renzo Fernando (2021072615)**
- **Vargas Candia, Hashira Belén (2022075480)**

**Tacna – Perú**  
**2026**

---

# Sistema Agente de IA para Revisión y Asesoría de Tesis
## Informe de Factibilidad
**Versión 1.0**

### Control de versiones
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| --- | --- | --- | --- | --- | --- |
| 1.0 | - | - | - | 10/04/2025 | Versión original |

---

# Índice general
- [1. Descripción del Proyecto](#1-descripción-del-proyecto)
  - [1.1 Nombre del proyecto](#11-nombre-del-proyecto)
  - [1.2 Duración del proyecto](#12-duración-del-proyecto)
  - [1.3 Descripción](#13-descripción)
  - [1.4 Objetivos](#14-objetivos)
- [2. Riesgos](#2-riesgos)
- [3. Análisis de la situación actual](#3-análisis-de-la-situación-actual)
- [4. Estudio de factibilidad](#4-estudio-de-factibilidad)
  - [4.1 Factibilidad técnica](#41-factibilidad-técnica)
  - [4.2 Factibilidad económica](#42-factibilidad-económica)
  - [4.3 Factibilidad operativa](#43-factibilidad-operativa)
  - [4.4 Factibilidad legal](#44-factibilidad-legal)
  - [4.5 Factibilidad ambiental](#45-factibilidad-ambiental)
- [5. Análisis financiero](#5-análisis-financiero)
- [6. Conclusiones](#6-conclusiones)

---

# Informe de Factibilidad

## 1. Descripción del Proyecto

### 1.1 Nombre del proyecto
Sistema Agente de IA para Revisión y Asesoría de Tesis.

### 1.2 Duración del proyecto
| Fases | Duración |
| --- | --- |
| Inicio | Del 31/03/2026 al 04/04/2026 |
| Elaboración | Del 05/04/2026 al 05/05/2026 |
| Construcción | Del 06/05/2026 al 31/05/2026 |
| Transición | Del 01/06/2026 al 18/06/2026 |

### 1.3 Descripción
El sistema tiene como propósito modernizar y agilizar el proceso de revisión de tesis universitarias. Actualmente, los tesistas sufren largas esperas para recibir retroalimentación, y los asesores están saturados de trabajo. Con este nuevo sistema web, se busca brindar una plataforma impulsada por Inteligencia Artificial (mediante LLMs como Gemini u OpenAI) que permita preevaluar la redacción, el formato (APA, IEEE, etc.), la coherencia metodológica y detectar posibles plagios, sirviendo como un coasesor disponible 24/7.

### 1.4 Objetivos
#### 1.4.1 Objetivo general
Desarrollar e implementar un Agente de IA web que optimice los tiempos de revisión de tesis, mejorando la calidad académica de los documentos y reduciendo la carga operativa de los asesores humanos.

#### 1.4.2 Objetivos específicos
- Implementar un módulo de procesamiento de lenguaje natural (NLP) para analizar estructura, coherencia y formato de documentos académicos (PDF/Word).
- Permitir el registro y autenticación segura de usuarios (estudiantes y asesores).
- Generar reportes automáticos detallados con sugerencias de mejora y correcciones ortotipográficas.

## 2. Riesgos
Los riesgos identificados en el proyecto se pueden clasificar en tres categorías de acuerdo con su frecuencia y efectos potenciales:

| Frecuencia de riesgo | Valores |
| --- | --- |
| Bajo | 1 |
| Medio | 2 |
| Alto | 3 |

| Riesgo | Valor | Efecto |
| --- | --- | --- |
| Privacidad de datos: filtración de investigaciones inéditas al procesarlas a través de APIs de terceros | 3 | Catastrófico |
| Alucinaciones de la IA: que el agente sugiera bibliografía falsa o correcciones metodológicas incorrectas | 2 | Serio |
| Costos de API: incremento de costos operativos si los usuarios suben documentos demasiado pesados de forma constante | 1 | Moderado |
| Rechazo institucional: que las universidades o asesores consideren el uso de la IA como una falta a la ética académica | 2 | Serio |

## 3. Análisis de la situación actual

### 3.1 Planteamiento del problema
El modelo actual de asesoría de tesis es un cuello de botella en las universidades. Los asesores humanos tienen múltiples alumnos y poco tiempo, lo que genera retrasos de semanas para una simple revisión de formato o redacción. Esto causa frustración, prolonga el tiempo de titulación y disminuye la calidad de las investigaciones por la falta de iteraciones rápidas.

### 3.2 Consideraciones de hardware y software
**Hardware:**
- **Computadora de desarrollo:** Procesador Intel Core i7 (o superior), 16 GB de RAM, SSD de 256 GB (mínimo) y monitor con resolución mínima de 1920x1080 píxeles.
- **Servidor VPS para despliegue:** vCPU de 4 núcleos (mínimo), 8 GB de RAM (mínimo), 100 GB SSD y sistema operativo Linux (Debian 12.10 o similar).

**Software:**
- Sistema Operativo: Windows 10 PRO.
- IDE: Visual Studio Code o similar.
- Servidor Web: Apache HTTP Server.
- Base de Datos: PostgreSQL.
- Lenguaje de Programación: PHP (puro, sin framework).
- Otras herramientas: JasperReports (opcional), Git y Consola SSH.

## 4. Estudio de factibilidad
El estudio de factibilidad del proyecto tiene como objetivo evaluar la viabilidad del proyecto desde varias perspectivas: técnica, económica, operativa y organizacional.

### 4.1 Factibilidad técnica
El estudio de factibilidad técnica evalúa si los recursos tecnológicos disponibles permiten el desarrollo e implementación del sistema de manera eficiente y segura. El desarrollo se realizará localmente con equipos adecuados para tareas de codificación y pruebas. Se utilizará PHP puro y PostgreSQL, tecnologías compatibles con entornos de producción web. El despliegue final se contempla en una VPS con servidor Apache. La seguridad incluirá validación de datos, cifrado de contraseñas y protección contra inyecciones SQL. El uso de Git permitirá el control de versiones y la integridad del código.

### 4.2 Factibilidad económica
#### 4.2.1 Costos generales
Incluye insumos como papel bond, tinta, lapiceros y accesorios, con un total estimado de S/. 195.00.

#### 4.2.2 Costos operativos durante el desarrollo
Incluye servicios de luz (S/. 240.00) e Internet (S/. 210.00) por 3 meses, sumando S/. 450.00.

#### 4.2.3 Costos del ambiente
Incluye dominio web (S/. 55.00), VPS por 3 meses (S/. 180.00) y certificado SSL (S/. 80.00), totalizando S/. 315.00.

#### 4.2.4 Costos de personal
Contempla 4 roles (Backend, Frontend, UI/UX y Analista) con 220 horas estimadas cada uno a una tarifa de S/. 2.27 por hora, resultando en S/. 2,000.00 en total.

#### 4.2.5 Costos totales del desarrollo del sistema
El costo total del proyecto asciende a S/. 2,960.00.

### 4.3 Factibilidad operativa
El sistema busca automatizar el acceso a la información y brindar seguimiento individualizado. Se diseñará para ser intuitivo y accesible desde cualquier dispositivo con internet. El personal será capacitado en el registro de información y generación de reportes para garantizar una correcta adopción.

### 4.4 Factibilidad legal
El proyecto debe cumplir con la Ley de Protección de Datos Personales. Se establecerán políticas de privacidad y términos de uso, requiriendo el consentimiento explícito de los usuarios. El uso de tecnologías de código abierto evita conflictos de licencias privativas.

### 4.5 Factibilidad ambiental
El proyecto reduce el uso de papel al digitalizar documentación. Optimiza la energía mediante el uso de servidores eficientes y promueve la movilidad sostenible al permitir gestiones 100% en línea.

## 5. Análisis financiero

### 5.1 Justificación de la inversión
Se espera aumentar el número de usuarios al facilitar el acceso a la información y reducir la carga operativa mediante la digitalización.

### 5.1.2 Criterios de inversión
Dada la naturaleza del proyecto, se realiza una evaluación cualitativa con una inversión estimada de S/. 855.00 (costos de ambiente y operativos), riesgo financiero bajo y beneficio estratégico alto.

## 6. Conclusiones
- El proyecto es viable técnica, económica, operativa y legalmente.
- Resuelve ineficiencias en procesos manuales y falta de transparencia.
- Los riesgos son manejables con atención a la seguridad y control de costos.
- Beneficia al medio ambiente al reducir papel y desplazamientos físicos.

---

## Contenido original (recuperado)

![Logo UPT](./media/logo-upt.png)

# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERÍA
### Escuela Profesional de Ingeniería de Sistemas

**Proyecto:** "Agente de IA para Revisión y Asesoría de Tesis"

**Curso:** Patrones de Software  
**Docente:** Ing. Patrick Cuadros Quiroga

**Integrantes:**
- **Ayala Ramos, Carlos Daniel (2022074266)**
- **Loyola Vilca, Renzo Fernando (2021072615)**
- **Vargas Candia, Hashira Belén (2022075480)**

**Tacna – Perú**  
**2026**

---

# Sistema Agente de IA para Revisión y Asesoría de Tesis
## Informe de Factibilidad
**Versión 1.0**

### Control de versiones
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| --- | --- | --- | --- | --- | --- |
| 1.0 | - | - | - | 10/04/2025 | Versión original |

---

# Índice general
- [1. Descripción del Proyecto](#1-descripción-del-proyecto)
  - [1.1 Nombre del proyecto](#11-nombre-del-proyecto)
  - [1.2 Duración del proyecto](#12-duración-del-proyecto)
  - [1.3 Descripción](#13-descripción)
  - [1.4 Objetivos](#14-objetivos)
- [2. Riesgos](#2-riesgos)
- [3. Análisis de la situación actual](#3-análisis-de-la-situación-actual)
- [4. Estudio de factibilidad](#4-estudio-de-factibilidad)
  - [4.1 Factibilidad técnica](#41-factibilidad-técnica)
  - [4.2 Factibilidad económica](#42-factibilidad-económica)
  - [4.3 Factibilidad operativa](#43-factibilidad-operativa)
  - [4.4 Factibilidad legal](#44-factibilidad-legal)
  - [4.5 Factibilidad ambiental](#45-factibilidad-ambiental)
- [5. Análisis financiero](#5-análisis-financiero)
- [6. Conclusiones](#6-conclusiones)

---

# Informe de Factibilidad

## 1. Descripción del Proyecto

### 1.1 Nombre del proyecto
Sistema Agente de IA para Revisión y Asesoría de Tesis.

### 1.2 Duración del proyecto
| Fases | Duración |
| --- | --- |
| Inicio | Del 31/03/2026 al 04/04/2026 |
| Elaboración | Del 05/04/2026 al 05/05/2026 |
| Construcción | Del 06/05/2026 al 31/05/2026 |
| Transición | Del 01/06/2026 al 18/06/2026 |

### 1.3 Descripción
El sistema tiene como propósito modernizar y agilizar el proceso de revisión de tesis universitarias. Actualmente, los tesistas sufren largas esperas para recibir retroalimentación, y los asesores están saturados de trabajo. Con este nuevo sistema web, se busca brindar una plataforma impulsada por Inteligencia Artificial (mediante LLMs como Gemini u OpenAI) que permita preevaluar la redacción, el formato (APA, IEEE, etc.), la coherencia metodológica y detectar posibles plagios, sirviendo como un coasesor disponible 24/7.

### 1.4 Objetivos
#### 1.4.1 Objetivo general
Desarrollar e implementar un Agente de IA web que optimice los tiempos de revisión de tesis, mejorando la calidad académica de los documentos y reduciendo la carga operativa de los asesores humanos.

#### 1.4.2 Objetivos específicos
- Implementar un módulo de procesamiento de lenguaje natural (NLP) para analizar estructura, coherencia y formato de documentos académicos (PDF/Word).
- Permitir el registro y autenticación segura de usuarios (estudiantes y asesores).
- Generar reportes automáticos detallados con sugerencias de mejora y correcciones ortotipográficas.

## 2. Riesgos
Los riesgos identificados en el proyecto se pueden clasificar en tres categorías de acuerdo con su frecuencia y efectos potenciales:

| Frecuencia de riesgo | Valores |
| --- | --- |
| Bajo | 1 |
| Medio | 2 |
| Alto | 3 |

| Riesgo | Valor | Efecto |
| --- | --- | --- |
| Privacidad de datos: filtración de investigaciones inéditas al procesarlas a través de APIs de terceros | 3 | Catastrófico |
| Alucinaciones de la IA: que el agente sugiera bibliografía falsa o correcciones metodológicas incorrectas | 2 | Serio |
| Costos de API: incremento de costos operativos si los usuarios suben documentos demasiado pesados de forma constante | 1 | Moderado |
| Rechazo institucional: que las universidades o asesores consideren el uso de la IA como una falta a la ética académica | 2 | Serio |

## 3. Análisis de la situación actual

### 3.1 Planteamiento del problema
El modelo actual de asesoría de tesis es un cuello de botella en las universidades. Los asesores humanos tienen múltiples alumnos y poco tiempo, lo que genera retrasos de semanas para una simple revisión de formato o redacción. Esto causa frustración, prolonga el tiempo de titulación y disminuye la calidad de las investigaciones por la falta de iteraciones rápidas.

### 3.2 Consideraciones de hardware y software
**Hardware:**
- **Computadora de desarrollo:** Procesador Intel Core i7 (o superior), 16 GB de RAM, SSD de 256 GB (mínimo) y monitor con resolución mínima de 1920x1080 píxeles.
- **Servidor VPS para despliegue:** vCPU de 4 núcleos (mínimo), 8 GB de RAM (mínimo), 100 GB SSD y sistema operativo Linux (Debian 12.10 o similar).

**Software:**
- Sistema Operativo: Windows 10 PRO.
- IDE: Visual Studio Code o similar.
- Servidor Web: Apache HTTP Server.
- Base de Datos: PostgreSQL.
- Lenguaje de Programación: PHP (puro, sin framework).
- Otras herramientas: JasperReports (opcional), Git y Consola SSH.

## 4. Estudio de factibilidad
El estudio de factibilidad del proyecto tiene como objetivo evaluar la viabilidad del proyecto desde varias perspectivas: técnica, económica, operativa y organizacional.

### 4.1 Factibilidad técnica
El estudio de factibilidad técnica evalúa si los recursos tecnológicos disponibles permiten el desarrollo e implementación del sistema de manera eficiente y segura. El desarrollo se realizará localmente con equipos adecuados para tareas de codificación y pruebas. Se utilizará PHP puro y PostgreSQL, tecnologías compatibles con entornos de producción web. El despliegue final se contempla en una VPS con servidor Apache. La seguridad incluirá validación de datos, cifrado de contraseñas y protección contra inyecciones SQL. El uso de Git permitirá el control de versiones y la integridad del código.

### 4.2 Factibilidad económica
#### 4.2.1 Costos generales
Incluye insumos como papel bond, tinta, lapiceros y accesorios, con un total estimado de S/. 195.00.

#### 4.2.2 Costos operativos durante el desarrollo
Incluye servicios de luz (S/. 240.00) e Internet (S/. 210.00) por 3 meses, sumando S/. 450.00.

#### 4.2.3 Costos del ambiente
Incluye dominio web (S/. 55.00), VPS por 3 meses (S/. 180.00) y certificado SSL (S/. 80.00), totalizando S/. 315.00.

#### 4.2.4 Costos de personal
Contempla 4 roles (Backend, Frontend, UI/UX y Analista) con 220 horas estimadas cada uno a una tarifa de S/. 2.27 por hora, resultando en S/. 2,000.00 en total.

#### 4.2.5 Costos totales del desarrollo del sistema
El costo total del proyecto asciende a S/. 2,960.00.

### 4.3 Factibilidad operativa
El sistema busca automatizar el acceso a la información y brindar seguimiento individualizado. Se diseñará para ser intuitivo y accesible desde cualquier dispositivo con internet. El personal será capacitado en el registro de información y generación de reportes para garantizar una correcta adopción.

### 4.4 Factibilidad legal
El proyecto debe cumplir con la Ley de Protección de Datos Personales. Se establecerán políticas de privacidad y términos de uso, requiriendo el consentimiento explícito de los usuarios. El uso de tecnologías de código abierto evita conflictos de licencias privativas.

### 4.5 Factibilidad ambiental
El proyecto reduce el uso de papel al digitalizar documentación. Optimiza la energía mediante el uso de servidores eficientes y promueve la movilidad sostenible al permitir gestiones 100% en línea.

## 5. Análisis financiero

### 5.1 Justificación de la inversión
Se espera aumentar el número de usuarios al facilitar el acceso a la información y reducir la carga operativa mediante la digitalización.

### 5.1.2 Criterios de inversión
Dada la naturaleza del proyecto, se realiza una evaluación cualitativa con una inversión estimada de S/. 855.00 (costos de ambiente y operativos), riesgo financiero bajo y beneficio estratégico alto.

## 6. Conclusiones
- El proyecto es viable técnica, económica, operativa y legalmente.
- Resuelve ineficiencias en procesos manuales y falta de transparencia.
- Los riesgos son manejables con atención a la seguridad y control de costos.
- Beneficia al medio ambiente al reducir papel y desplazamientos físicos.

---
Informe original recuperado y anexado al final del documento.
