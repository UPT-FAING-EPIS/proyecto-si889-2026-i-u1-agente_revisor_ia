# Issues del Proyecto - Agente IA Revisor de Tesis

## [ISSUE 1] Registrar nuevo usuario en la plataforma

**Como** estudiante interesado en usar la plataforma  
**Quiero** registrarme con mi correo electrónico y contraseña  
**Para** crear una cuenta y acceder a los servicios de asesoramiento de tesis

### Criterios de Aceptación

- [ ] El formulario debe validar que el email tenga formato correcto
- [ ] La contraseña debe tener al menos 6 caracteres
- [ ] El sistema debe enviar un correo de confirmación (si está habilitado)
- [ ] Los datos deben guardarse de forma segura en Supabase
- [ ] El usuario debe recibir un token de acceso tras el registro exitoso
- [ ] Se debe mostrar un mensaje de error claro si el email ya existe

### Escenarios de Prueba

```gherkin
Escenario: Registro exitoso con email válido
DADO que estoy en la página de registro
CUANDO ingreso un email válido "estudiante@example.com"
Y ingreso una contraseña de 8 caracteres "Passwor123"
Y hago clic en "Crear Cuenta"
ENTONCES el sistema valida los datos exitosamente
Y crea la cuenta en Supabase
Y me muestra un mensaje de confirmación
Y me redirige al login

Escenario: Registro falla con email inválido
DADO que estoy en la página de registro
CUANDO ingreso un email sin formato válido "estudianteexample"
Y ingreso una contraseña válida
Y hago clic en "Crear Cuenta"
ENTONCES el sistema muestra error "Email inválido"
Y no persiste la cuenta

Escenario: Registro falla con contraseña corta
DADO que estoy en la página de registro
CUANDO ingreso un email válido
Y ingreso una contraseña de 4 caracteres "Pass"
Y hago clic en "Crear Cuenta"
ENTONCES el sistema muestra error "Contraseña debe tener mínimo 6 caracteres"
Y no persiste la cuenta

Escenario: Registro falla - email ya registrado
DADO que ya existe un usuario con email "existe@example.com"
CUANDO intento registrar nuevamente con "existe@example.com"
Y ingreso una contraseña válida
Y hago clic en "Crear Cuenta"
ENTONCES el sistema muestra error "Este email ya está registrado"
Y no crea cuenta duplicada
```

---

## [ISSUE 2] Autenticar usuario con email y contraseña

**Como** estudiante registrado  
**Quiero** iniciar sesión con mis credenciales  
**Para** acceder a mi dashboard y mis documentos guardados

### Criterios de Aceptación

- [ ] El formulario debe validar email y contraseña
- [ ] El sistema debe verificar las credenciales contra Supabase
- [ ] Se debe devolver un token JWT válido tras login exitoso
- [ ] El token debe almacenarse en el navegador (localStorage o cookie segura)
- [ ] Se debe mostrar error específico si las credenciales son inválidas
- [ ] El usuario debe mantenerse autenticado hasta cerrar sesión
- [ ] La sesión debe expirar tras el tiempo configurado

### Escenarios de Prueba

```gherkin
Escenario: Login exitoso con credenciales válidas
DADO que estoy en la página de login
CUANDO ingreso email "estudiante@example.com"
Y ingreso contraseña correcta "Passwor123"
Y hago clic en "Iniciar Sesión"
ENTONCES el sistema verifica las credenciales en Supabase
Y devuelve un token JWT válido
Y almacena el token en localStorage
Y me redirige al dashboard
Y puedo ver mis documentos

Escenario: Login falla con credenciales inválidas
DADO que estoy en la página de login
CUANDO ingreso email "estudiante@example.com"
Y ingreso contraseña incorrecta "WrongPass"
Y hago clic en "Iniciar Sesión"
ENTONCES el sistema valida contra Supabase
Y muestra error "Email o contraseña incorrectos"
Y no me redirige al dashboard
Y el token no se almacena

Escenario: Login falla - usuario no existe
DADO que intento acceder con email no registrado
CUANDO ingreso email "noexiste@example.com"
Y ingreso cualquier contraseña
Y hago clic en "Iniciar Sesión"
ENTONCES el sistema muestra error "Usuario no registrado"
Y no se crea acceso

Escenario: Token se mantiene tras recargar página
DADO que he iniciado sesión correctamente
Y el token está almacenado en localStorage
CUANDO recargo la página
ENTONCES el frontend valida la sesión actual
Y me mantiene autenticado en el dashboard
Y no me fuerza a login nuevamente
```

---

## [ISSUE 3] Subir archivo PDF de tesis para procesamiento

**Como** estudiante  
**Quiero** subir mi archivo PDF de tesis a la plataforma  
**Para** que se procese y quede disponible para consultas con el asesor IA

### Criterios de Aceptación

- [ ] El sistema solo debe aceptar archivos en formato PDF
- [ ] El archivo debe validarse antes de subirse (no vacío, formato correcto)
- [ ] Se debe extraer el texto completo del PDF
- [ ] El texto debe dividirse en fragmentos (chunks) coherentes
- [ ] Se debe almacenar el PDF en el storage de Supabase
- [ ] Se muestra progreso de carga al usuario
- [ ] Se debe mostrar número de fragmentos extraídos
- [ ] Se debe mostrar error claro si la extracción falla
- [ ] La tesis debe asociarse al usuario autenticado

### Escenarios de Prueba

```gherkin
Escenario: Subida exitosa de PDF válido
DADO que estoy en el dashboard
Y tengo un archivo "tesis_final.pdf" válido
CUANDO arrastro el archivo a la zona de carga
Y hago clic en "Subir"
ENTONCES el sistema valida que sea PDF
Y inicia la extracción de texto
Y divide el texto en 45 fragmentos coherentes
Y almacena el PDF en Supabase storage
Y muestra "Tesis procesada exitosamente (45 fragmentos)"
Y el documento aparece en mi lista

Escenario: Rechazo de archivo no PDF
DADO que estoy en el dashboard
Y tengo un archivo "documento.docx"
CUANDO intento subir el archivo
ENTONCES el sistema valida el formato
Y muestra error "Solo se aceptan archivos PDF"
Y no procesa el archivo

Escenario: Rechazo de archivo PDF vacío
DADO que tengo un archivo "vacio.pdf" sin contenido
CUANDO intento subir el archivo
ENTONCES el sistema valida el contenido
Y muestra error "El archivo PDF está vacío"
Y no persiste el documento

Escenario: Rechazo de PDF escaneado sin OCR
DADO que tengo un PDF escaneado "tesis_escaneada.pdf" sin texto extraíble
CUANDO intento subir el archivo
ENTONCES el sistema intenta extraer texto
Y muestra error "No se encontró texto legible en el PDF. Verifica que no sea escaneado"
Y no persiste el documento

Escenario: Reemplazo de tesis anterior
DADO que ya tengo una tesis cargada "tesis_v1.pdf"
Y tengo una versión actualizada "tesis_v2.pdf"
CUANDO subo la nueva versión
Y selecciono "Reemplazar tesis anterior"
ENTONCES el sistema elimina la versión anterior
Y sustituyela con la nueva
Y preserva el historial de conversaciones (opcional)
Y muestra confirmación del reemplazo
```

---

## [ISSUE 4] Chatear con asesor IA usando contexto de tesis (RAG)

**Como** estudiante  
**Quiero** hacer preguntas sobre mi tesis al asesor IA  
**Para** obtener retroalimentación contextualizada basada en el contenido de mi documento

### Criterios de Aceptación

- [ ] El sistema debe buscar fragmentos relevantes de la tesis (búsqueda vectorial)
- [ ] La respuesta debe basarse en los fragmentos encontrados
- [ ] Las respuestas deben mostrarse en tiempo real (streaming)
- [ ] Se debe mantener el historial de conversación en la sesión
- [ ] El usuario puede crear múltiples sesiones de chat
- [ ] Se debe mostrar indicador mientras el IA está procesando
- [ ] La respuesta no debe tomar más de 30 segundos
- [ ] Se debe guardar cada mensaje en la base de datos

### Escenarios de Prueba

```gherkin
Escenario: Chat exitoso con IA - búsqueda RAG
DADO que tengo una tesis cargada en la plataforma
Y estoy en la ventana de chat
CUANDO escribo la pregunta "¿Cuál es la hipótesis general de mi tesis?"
Y presiono Enter o hago clic en enviar
ENTONCES el sistema genera embedding de la pregunta
Y busca fragmentos similares en pgvector
Y selecciona los 3-5 fragmentos más relevantes
Y envía fragmentos + pregunta + historial a Gemini
Y la IA genera respuesta contextualizando con esos fragmentos
Y la respuesta se muestra en streaming (palabras por palabras)
Y el mensaje se guarda en el historial
Y aparece el mensaje con timestamp

Escenario: Respuesta cuando hay contexto insuficiente
DADO que tengo una tesis cargada
CUANDO pregunto algo fuera del contexto de la tesis "¿Cuál es la capital de Francia?"
ENTONCES el sistema busca fragmentos relevantes
Y encuentra pocos/ningún fragmento relacionado
Y la IA responde explícitamente "No encuentro información sobre esto en tu tesis"
Y sugiere hacer preguntas sobre el contenido del documento

Escenario: Mantenimiento de historial en sesión
DADO que he hecho 3 preguntas anteriormente
Y estoy en la misma sesión de chat
CUANDO hago una nueva pregunta "¿Cómo puedo mejorar el marco teórico?"
ENTONCES el sistema incluye los últimos mensajes en el historial (hasta 40 mensajes)
Y transmite contexto histórico a Gemini
Y la IA genera respuesta considerando conversaciones previas
Y el nuevo mensaje se añade al historial

Escenario: Timeout de respuesta
DADO que la API de Gemini retrasa la respuesta más de 30 segundos
CUANDO el usuario espera por la respuesta
ENTONCES después de timeout
Y el sistema muestra error "No se pudo completar la respuesta. Intenta de nuevo"
Y se detiene el streaming
Y se permite al usuario reintentar

Escenario: Crear nueva sesión de chat
DADO que ya tengo una sesión activa con varios mensajes
CUANDO hago clic en "Nueva Conversación"
ENTONCES el sistema crea nueva sesión de chat en BD
Y limpia el historial de la UI
Y asigna nuevo chat_id
Y la sesión anterior se preserva en el historial
```

---

## [ISSUE 5] Revisión especializada de tesis según normas FAING

**Como** estudiante de FAING  
**Quiero** obtener una revisión profunda de mi tesis según el Manual FAING  
**Para** cumplir con los estándares de calidad y rigor metodológico exigidos

### Criterios de Aceptación

- [ ] El sistema debe usar el prompt especializado FAING (no generic)
- [ ] La revisión debe evaluar: título, hipótesis, marco teórico, metodología, resultados
- [ ] Se debe validar alineación entre problema-objetivos-hipótesis
- [ ] Se debe verificar uso correcto de normas APA en referencias
- [ ] Se debe evaluar rigor metodológico y coherencia lógica
- [ ] La revisión puede procesar hasta 260KB de texto
- [ ] Se debe limitar a máximo 6144 tokens de salida
- [ ] Se debe mostrar progreso de la revisión

### Escenarios de Prueba

```gherkin
Escenario: Revisión exitosa - evaluación FAING completa
DADO que estoy en modo "Revisión de Tesis"
Y tengo cargada una tesis bien formada
CUANDO hago clic en "Solicitar Revisión Completa"
Y confirmo que deseo evaluar con criterios FAING
ENTONCES el sistema extrae el texto de la tesis
Y valida que no supere 260KB
Y envía solicitud con prompt especializado FAING a Gemini
Y Gemini evalúa: título, matriz de consistencia, marco teórico, metodología, referencias APA
Y devuelve feedback detallado del revisor IA
Y muestra la revisión de manera estructurada
Y guarda la revisión en la sesión

Escenario: Revisión detecta problemas de alineación
DADO que tengo una tesis con incongruencia entre problema-objetivo-hipótesis
CUANDO solicito revisión FAING
ENTONCES el sistema valida la matriz de consistencia
Y Gemini identifica la falta de alineación
Y propone ajustes específicos según el manual FAING
Y muestra recomendaciones accionables
Y el estudiante puede iterar en la revisión

Escenario: Revisión detecta deficiencias en referencias APA
DADO que tengo una tesis con citas mal formateadas (no APA)
CUANDO solicito revisión
ENTONCES el sistema evalúa el formato de referencias
Y Gemini identifica errores (falta de DOI, fechas incorrectas, etc)
Y proporciona ejemplos de citas correctas en APA
Y sugiere mínimo 25-35 referencias requeridas

Escenario: Tesis excede límite de procesamiento
DADO que tengo una tesis muy extensa (>260KB de texto)
CUANDO solicito revisión FAING
ENTONCES el sistema valida el tamaño
Y muestra error "Tesis demasiado extensa. Límite: 260KB"
Y sugiere dividir el análisis por secciones
Y permite seleccionar secciones específicas para revisar
```

---

## [ISSUE 6] Listar documentos cargados por usuario

**Como** estudiante  
**Quiero** ver la lista de tesis/documentos que he cargado  
**Para** acceder rápidamente a los que deseo consultar

### Criterios de Aceptación

- [ ] Solo se muestran documentos del usuario autenticado
- [ ] Se debe mostrar nombre del archivo, fecha de carga y cantidad de fragmentos
- [ ] Se debe permitir seleccionar un documento para abrir
- [ ] Se debe mostrar URL descargable del PDF
- [ ] Se debe estar operativo a nivel de pagináción si hay muchos docs
- [ ] Se debe permitir eliminar documentos

### Escenarios de Prueba

```gherkin
Escenario: Listar documentos del usuario
DADO que estoy autenticado
Y he cargado 3 tesis
CUANDO accedo a la sección "Mis Documentos"
ENTONCES el sistema consulta documentos del usuario desde Supabase
Y muestra lista con:
  | Nombre | Fecha Carga | Fragmentos | Acciones|
  | tesis_final.pdf | 2026-04-20 | 45 | Abrir, Descargar, Eliminar |
  | tesis_v1.pdf | 2026-04-18 | 38 | Abrir, Descargar, Eliminar |
  | ensayo.pdf | 2026-04-15 | 12 | Abrir, Descargar, Eliminar |
Y permite hacer clic en el nombre para abrir

Escenario: Documento aparece inmediatamente tras subida
DADO que acabo de subir un documento exitosamente
CUANDO regreso a "Mis Documentos"
ENTONCES el documento nuevo aparece en la lista
Y muestra los fragmentos procesados
Y está disponible para chat inmediatamente

Escenario: Eliminar documento
DADO que tengo un documento en la lista
CUANDO hago clic en "Eliminar"
Y confirmo la acción
ENTONCES el sistema elimina el documento y sus fragmentos de BD
Y elimina el PDF del storage
Y refresca la lista
Y muestra confirmación "Documento eliminado"
```

---

## [ISSUE 7] Ver y descargar PDF de tesis cargada

**Como** estudiante  
**Quiero** ver en tiempo real el PDF que cargué y poder descargarlo  
**Para** consultarlo mientras chateo con el asesor IA

### Criterios de Aceptación

- [ ] El PDF debe mostrarse en un visor integrado (no download forzado)
- [ ] Se debe permitir navegar entre páginas
- [ ] Se debe poder hacer zoom in/out
- [ ] Se debe poder descargar el PDF original
- [ ] El visor debe estar visible mientras escribo preguntas
- [ ] La URL del PDF debe ser de corta duración (1 hora por defecto)

### Escenarios de Prueba

```gherkin
Escenario: Visualizar PDF en el visor integrado
DADO que tengo un documento cargado
CUANDO selecciono el documento
Y abro la sección "Ver Tesis"
ENTONCES se genera URL firmada temporal del PDF
Y se muestra el PDF en un visor integrado
Y puedo navegar entre páginas (anterior/siguiente)
Y puedo ver el número de páginas actual
Y puedo hacer zoom (zoom in/out)
Y la interfaz se mantiene responsive

Escenario: Descargar PDF original
DADO que visualizo un PDF en el visor
CUANDO hago clic en "Descargar"
ENTONCES el sistema genera un enlace de descarga firmado
Y el navegador descarga el archivo PDF original
Y la descarga incluye el nombre de archivo original

Escenario: URL de PDF expira por seguridad
DADO que generé un URL firmada para el PDF hace más de 1 hora
CUANDO intento acceder a esa URL
ENTONCES la URL ha expirado por seguridad
Y el sistema genera una nueva URL al solicitar el documento
Y se muestra el PDF correctamente
```

---

## [ISSUE 8] Crear y gestionar sesiones de chat independientes

**Como** estudiante  
**Quiero** mantener múltiples conversaciones independientes con el asesor  
**Para** explorar diferentes temas y comparar perspectivas

### Criterios de Aceptación

- [ ] Se debe poder crear una nueva sesión de chat
- [ ] Cada sesión tiene su propio ID y historial independiente
- [ ] Se debe ver lista de sesiones por documento
- [ ] Se debe poder cambiar entre sesiones sin perder historial
- [ ] Se debe poder eliminar una sesión
- [ ] Se debe poder renombrar una sesión
- [ ] Las sesiones se guardan en Supabase

### Escenarios de Prueba

```gherkin
Escenario: Crear nueva sesión de chat
DADO que estoy viendo un documento
CUANDO hago clic en "Nueva Conversación"
ENTONCES el sistema crea nueva sesión_chat en la BD
Y asigna un ID único
Y la sesión se inicializa con historial vacío
Y se selecciona la nueva sesión como activa
Y el input de chat se limpia

Escenario: Cambiar entre sesiones
DADO que tengo 3 sesiones de chat activas
CUANDO hago clic en una sesión anterior
ENTONCES se carga el historial de esa sesión
Y los mensajes anteriores se muestran
Y el contexto RAG se actualiza a esa sesión
Y puedo continuar la conversación desde donde la dejé

Escenario: Eliminar una sesión
DADO que tengo una sesión que deseo eliminar
CUANDO hago clic derecho en la sesión
Y selecciono "Eliminar"
Y confirmo la acción
ENTONCES el sistema elimina la sesión de BD
Y elimina todos los mensajes asociados
Y la sesión desaparece de la lista
Y si era la activa, se cambia a otra sesión

Escenario: Renombrar sesión
DADO que tengo una sesión con nombre genérico "Sesión 1"
CUANDO hago doble clic en el nombre
Y escribo "Revisión de Metodología"
Y presiono Enter
ENTONCES el sistema actualiza el nombre en BD
Y se refleja el cambio inmediatamente en la UI
```

---

## [ISSUE 9] Validar autenticación y bloquear acceso no autorizado

**Como** desarrollador/administrador  
**Quiero** que el sistema valide tokens JWT en cada petición  
**Para** asegurar que solo usuarios autenticados accedan a recursos protegidos

### Criterios de Aceptación

- [ ] Cada endpoint protegido debe verificar token JWT
- [ ] Token inválido debe devolver error 401
- [ ] Token expirado debe devolver error 401
- [ ] Falta de token debe devolver error 401
- [ ] Se debe validar que el usuario sea el propietario del recurso
- [ ] Acceso a recurso de otro usuario debe devolver error 403

### Escenarios de Prueba

```gherkin
Escenario: Acceso permitido con token válido
DADO que tengo un token JWT válido
Y el token no está expirado
CUANDO accedo a GET /api/documents
ENTONCES el middleware valida el token
Y extrae el user_id del token
Y el endpoint devuelve los documentos del usuario
Y recibo estado 200

Escenario: Acceso denegado - sin token
DADO que no envío token en la petición
CUANDO intento acceder a GET /api/documents
ENTONCES el middleware detecta falta de token
Y devuelve error 401 "Token no proporcionado"
Y no devuelve documentos

Escenario: Acceso denegado - token inválido
DADO que envío un token malformado "invalid.token.here"
CUANDO intento acceder a GET /api/documents
ENTONCES el middleware intenta validar el token
Y detecta que es inválido
Y devuelve error 401 "Token inválido"

Escenario: Acceso denegado - token expirado
DADO que tengo un token que expiró hace 1 hora
CUANDO intento acceder a GET /api/documents
ENTONCES el middleware valida la fecha de expiración
Y detecta que está expirado
Y devuelve error 401 "Token expirado"

Escenario: Prohibición de acceso - recurso de otro usuario
DADO que estoy autenticado como usuario_A
Y getUserId() devuelve "user_123"
Y existe un documento perteneciente a usuario_B
CUANDO intento acceder a GET /api/documents/doc_456
Y doc_456 tiene user_id = "user_999"
ENTONCES el sistema verifica propiedad del recurso
Y detecta que no me pertenece
Y devuelve error 403 "Acceso prohibido"
```

---

## [ISSUE 10] Manejo robusto de errores y validaciones

**Como** usuario de la plataforma  
**Quiero** recibir mensajes de erro claros y amigables  
**Para** entender qué salió mal y cómo puedo corregirlo

### Criterios de Aceptación

- [ ] Todos los errores deben tener mensajes claros en español
- [ ] Errores de validación deben listar campos específicos
- [ ] Errores de servicio externo deben mostrar fallback amigable
- [ ] No se deben exponer detalles técnicos al usuario
- [ ] Se debe loguear el error completo en servidor
- [ ] Timeout de respuestas se debe manejar gracefully

### Escenarios de Prueba

```gherkin
Escenario: Error de validación - campos requeridos
DADO que estoy en el formulario de login
CUANDO intento enviar sin llenar el email
Y hago clic en "Iniciar Sesión"
ENTONCES el sistema valida los campos
Y muestra error "El email es requerido"
Y destaca el campo faltante
Y no envía petición al servidor

Escenario: Error de API externa - Gemini no disponible
DADO que hago una pregunta al asesor IA
CUANDO la API de Gemini está temporalmente no disponible
ENTONCES el backend captura el error
Y muestra al usuario "No se pudo completar la respuesta en este momento. Intenta de nuevo"
Y loguea el error completo (stack trace)
Y no expone detalles técnicos al cliente

Escenario: Error de Supabase - conexión
DADO que intento listar mis documentos
CUANDO la conexión a Supabase falla
ENTONCES el backend captura el error SupabaseRepositoryError
Y muestra al usuario "Error al conectar con base de datos"
Y loguea la excepción completa
Y permite reintentar la acción

Escenario: Timeout de carga larga
DADO que subo un PDF muy grande (50MB)
Y el timeout está configurado en 30 segundos
CUANDO pasan 30 segundos sin completar la carga
ENTONCES se interrumpe la petición
Y muestra al usuario "La carga tardó demasiado. Intenta con un archivo más pequeño"
Y no persiste upload incompleto
```

---

# Instrucciones para crear los issues en GitHub

Ejecuta los siguientes comandos en terminal:

```bash
cd /workspaces/proyecto-si889-2026-i-u1-agente_revisor_ia

# Crear labels (opcional pero recomendado)
gh label create "user-story" --description "User story de feature" --color "0075ca"
gh label create "acceptance-criteria" --description "Criterios de aceptación definidos" --color "c5def5"
gh label create "gherkin-scenarios" --description "Escenarios en formato Gherkin" --color "f1e6b5"
gh label create "backend" --color "d73a49"
gh label create "frontend" --color "0366d6"

# Crear los issues
gh issue create \
  --title "Registrar nuevo usuario en la plataforma" \
  --body "$(cat << 'EOF'
**Como** estudiante interesado en usar la plataforma  
**Quiero** registrarme con mi correo electrónico y contraseña  
**Para** crear una cuenta y acceder a los servicios de asesoramiento de tesis

[Ver criterios y escenarios completos en la documentación del proyecto]
EOF
)" \
  --label "user-story,backend,frontend"

# Repetir para cada issue...
```

O si prefieres alternativa más simple:
```bash
# Ir al repo en GitHub y crear manualmente desde la interfaz web
# Copiar/pegar el contenido de cada issue del archivo GITHUB_ISSUES.md
```
