#!/usr/bin/env python3
"""Script para crear issues en GitHub con formato User Story + Gherkin"""

import subprocess
import json

REPO_OWNER = "UPT-FAING-EPIS"
REPO_NAME = "si889_2026-i-proyecto_si889_2026-i-u1-proyecto-formatos-01"

issues = [
    {
        "title": "Registrar nuevo usuario en la plataforma",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante interesado en usar la plataforma  
**Quiero** registrarme con mi correo electrónico y contraseña  
**Para** crear una cuenta y acceder a los servicios de asesoramiento de tesis

## Criterios de Aceptación

- [ ] El formulario debe validar que el email tenga formato correcto
- [ ] La contraseña debe tener al menos 6 caracteres
- [ ] El sistema debe enviar un correo de confirmación (si está habilitado)
- [ ] Los datos deben guardarse de forma segura en Supabase
- [ ] El usuario debe recibir un token de acceso tras el registro exitoso
- [ ] Se debe mostrar un mensaje de error claro si el email ya existe

## Escenarios de Prueba (Gherkin)

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
CUANDO ingreso una contraseña de 4 caracteres "Pass"
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
```"""
    },
    {
        "title": "Autenticar usuario con email y contraseña",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante registrado  
**Quiero** iniciar sesión con mis credenciales  
**Para** acceder a mi dashboard y mis documentos guardados

## Criterios de Aceptación

- [ ] El formulario debe validar email y contraseña
- [ ] El sistema debe verificar las credenciales contra Supabase
- [ ] Se debe devolver un token JWT válido tras login exitoso
- [ ] El token debe almacenarse en el navegador (localStorage o cookie segura)
- [ ] Se debe mostrar error específico si las credenciales son inválidas
- [ ] El usuario debe mantenerse autenticado hasta cerrar sesión
- [ ] La sesión debe expirar tras el tiempo configurado

## Escenarios de Prueba (Gherkin)

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

Escenario: Token se mantiene tras recargar página
DADO que he iniciado sesión correctamente
Y el token está almacenado en localStorage
CUANDO recargo la página
ENTONCES el frontend valida la sesión actual
Y me mantiene autenticado en el dashboard
Y no me fuerza a login nuevamente
```"""
    },
    {
        "title": "Subir archivo PDF de tesis para procesamiento",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante  
**Quiero** subir mi archivo PDF de tesis a la plataforma  
**Para** que se procese y quede disponible para consultas con el asesor IA

## Criterios de Aceptación

- [ ] El sistema solo debe aceptar archivos en formato PDF
- [ ] El archivo debe validarse antes de subirse (no vacío, formato correcto)
- [ ] Se debe extraer el texto completo del PDF
- [ ] El texto debe dividirse en fragmentos (chunks) coherentes
- [ ] Se debe almacenar el PDF en el storage de Supabase
- [ ] Se muestra progreso de carga al usuario
- [ ] Se debe mostrar número de fragmentos extraídos
- [ ] Se debe mostrar error claro si la extracción falla

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Subida exitosa de PDF válido
DADO que estoy en el dashboard
Y tengo un archivo "tesis_final.pdf" válido
CUANDO arrastro el archivo a la zona de carga
Y hago clic en "Subir"
ENTONCES el sistema valida que sea PDF
Y inicia la extracción de texto
Y divide el texto en fragmentos coherentes
Y almacena el PDF en Supabase storage
Y muestra confirmación de procesamiento

Escenario: Rechazo de archivo no PDF
DADO que tengo un archivo "documento.docx"
CUANDO intento subir el archivo
ENTONCES el sistema valida el formato
Y muestra error "Solo se aceptan archivos PDF"
Y no procesa el archivo

Escenario: Rechazo de PDF vacío
DADO que tengo un archivo "vacio.pdf" sin contenido
CUANDO intento subir el archivo
ENTONCES el sistema valida el contenido
Y muestra error "El archivo PDF está vacío"
Y no persiste el documento

Escenario: Rechazo de PDF escaneado sin OCR
DADO que tengo un PDF escaneado sin texto extraíble
CUANDO intento subir el archivo
ENTONCES el sistema intenta extraer texto
Y muestra error "No se encontró texto legible en el PDF"
```"""
    },
    {
        "title": "Chatear con asesor IA usando contexto de tesis (RAG)",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante  
**Quiero** hacer preguntas sobre mi tesis al asesor IA  
**Para** obtener retroalimentación contextualizada basada en mi documento

## Criterios de Aceptación

- [ ] El sistema debe buscar fragmentos relevantes de la tesis (búsqueda vectorial)
- [ ] La respuesta debe basarse en los fragmentos encontrados
- [ ] Las respuestas deben mostrarse en tiempo real (streaming)
- [ ] Se debe mantener el historial de conversación en la sesión
- [ ] El usuario puede crear múltiples sesiones de chat
- [ ] Se debe mostrar indicador mientras el IA está procesando
- [ ] La respuesta no debe tomar más de 30 segundos
- [ ] Se debe guardar cada mensaje en la base de datos

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Chat exitoso con IA - búsqueda RAG
DADO que tengo una tesis cargada
Y estoy en la ventana de chat
CUANDO escribo la pregunta "¿Cuál es la hipótesis general?"
Y presiono Enter
ENTONCES el sistema genera embedding de la pregunta
Y busca fragmentos similares en pgvector
Y la IA genera respuesta contextualizando
Y la respuesta se muestra en streaming
Y el mensaje se guarda en el historial

Escenario: Respuesta cuando hay contexto insuficiente
DADO que tengo una tesis cargada
CUANDO pregunto algo fuera del contexto
ENTONCES la IA responde explícitamente
Y sugiere hacer preguntas sobre el contenido

Escenario: Mantenimiento de historial en sesión
DADO que he hecho 3 preguntas anteriormente
Y estoy en la misma sesión
CUANDO hago una nueva pregunta
ENTONCES el sistema incluye los últimos mensajes
Y la IA genera respuesta considerando contexto histórico
```"""
    },
    {
        "title": "Revisión especializada de tesis según normas FAING",
        "labels": ["user-story", "backend"],
        "body": """**Como** estudiante de FAING  
**Quiero** obtener una revisión profunda de mi tesis según el Manual FAING  
**Para** cumplir con los estándares de calidad exigidos

## Criterios de Aceptación

- [ ] El sistema debe usar el prompt especializado FAING
- [ ] La revisión debe evaluar: título, hipótesis, marco teórico, metodología, resultados
- [ ] Se debe validar alineación entre problema-objetivos-hipótesis
- [ ] Se debe verificar uso correcto de normas APA
- [ ] Se debe evaluar rigor metodológico
- [ ] La revisión puede procesar hasta 260KB de texto
- [ ] Se debe limitar a máximo 6144 tokens de salida

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Revisión exitosa - evaluación FAING completa
DADO que tengo cargada una tesis bien formada
CUANDO hago clic en "Solicitar Revisión Completa"
ENTONCES el sistema extrae el texto de la tesis
Y valida que no supere 260KB
Y envía solicitud con prompt especializado FAING
Y Gemini evalúa estructura, metodología, referencias
Y devuelve feedback detallado
Y muestra la revisión estructurada

Escenario: Revisión detecta problemas de alineación
DADO que tengo una tesis con incongruencia
CUANDO solicito revisión FAING
ENTONCES el sistema valida la matriz de consistencia
Y Gemini identifica la falta de alineación
Y propone ajustes específicos

Escenario: Tesis excede límite de procesamiento
DADO que tengo una tesis >260KB
CUANDO solicito revisión
ENTONCES el sistema valida el tamaño
Y muestra error y sugiere dividir por secciones
```"""
    },
    {
        "title": "Listar documentos cargados por usuario",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante  
**Quiero** ver la lista de tesis que he cargado  
**Para** acceder rápidamente a los que deseo consultar

## Criterios de Aceptación

- [ ] Solo se muestran documentos del usuario autenticado
- [ ] Se debe mostrar nombre del archivo, fecha y cantidad de fragmentos
- [ ] Se permite seleccionar un documento
- [ ] Se muestra URL descargable del PDF
- [ ] Se permite eliminar documentos

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Listar documentos del usuario
DADO que estoy autenticado
Y he cargado 3 tesis
CUANDO accedo a "Mis Documentos"
ENTONCES muestra lista con nombre, fecha y fragmentos
Y permite hacer clic para abrir

Escenario: Documento aparece tras subida
DADO que acabo de subir un documento
CUANDO regreso a "Mis Documentos"
ENTONCES el documento aparece en la lista
Y está disponible para chat inmediatamente

Escenario: Eliminar documento
DADO que tengo un documento en la lista
CUANDO hago clic en "Eliminar"
Y confirmo la acción
ENTONCES se elimina documento, chunks y PDF
Y se refresca la lista
```"""
    },
    {
        "title": "Ver y descargar PDF de tesis cargada",
        "labels": ["user-story", "frontend"],
        "body": """**Como** estudiante  
**Quiero** ver el PDF que cargué y poder descargarlo  
**Para** consultarlo mientras chateo con el asesor

## Criterios de Aceptación

- [ ] El PDF debe mostrarse en un visor integrado
- [ ] Se permite navegar entre páginas
- [ ] Se puede hacer zoom in/out
- [ ] Se puede descargar el PDF original
- [ ] El visor está visible mientras escribo preguntas
- [ ] La URL del PDF tiene duración limitada (1 hora)

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Visualizar PDF en visor integrado
DADO que tengo un documento cargado
CUANDO selecciono el documento
ENTONCES se genera URL firmada temporal
Y se muestra el PDF en visor integrado
Y puedo navegar entre páginas
Y puedo hacer zoom

Escenario: Descargar PDF original
DADO que visualizo un PDF
CUANDO hago clic en "Descargar"
ENTONCES se descarga el archivo PDF original

Escenario: URL de PDF expira por seguridad
DADO que generé URL hace más de 1 hora
CUANDO intento acceder
ENTONCES la URL ha expirado
Y se genera nueva URL al solicitar documento
```"""
    },
    {
        "title": "Crear y gestionar sesiones de chat independientes",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** estudiante  
**Quiero** mantener múltiples conversaciones independientes  
**Para** explorar diferentes temas y comparar perspectivas

## Criterios de Aceptación

- [ ] Se puede crear una nueva sesión de chat
- [ ] Cada sesión tiene su propio ID e historial independiente
- [ ] Se ve lista de sesiones por documento
- [ ] Se puede cambiar entre sesiones sin perder historial
- [ ] Se puede eliminar una sesión
- [ ] Se puede renombrar una sesión

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Crear nueva sesión de chat
DADO que estoy viendo un documento
CUANDO hago clic en "Nueva Conversación"
ENTONCES se crea nueva sesión en BD
Y asigna ID único
Y inicializa con historial vacío
Y se selecciona como activa

Escenario: Cambiar entre sesiones
DADO que tengo 3 sesiones activas
CUANDO hago clic en una sesión anterior
ENTONCES carga el historial de esa sesión
Y muestra mensajes anteriores
Y puedo continuar desde donde la dejé

Escenario: Eliminar una sesión
DADO que tengo una sesión que deseo eliminar
CUANDO hago clic en "Eliminar"
Y confirmo la acción
ENTONCES se elimina de BD
Y desaparece de lista
```"""
    },
    {
        "title": "Validar autenticación y bloquear acceso no autorizado",
        "labels": ["user-story", "backend"],
        "body": """**Como** desarrollador/administrador  
**Quiero** que el sistema valide tokens JWT en cada petición  
**Para** asegurar que solo usuarios autenticados accedan a recursos protegidos

## Criterios de Aceptación

- [ ] Cada endpoint protegido verifica token JWT
- [ ] Token inválido devuelve error 401
- [ ] Token expirado devuelve error 401
- [ ] Falta de token devuelve error 401
- [ ] Valida que usuario sea propietario del recurso
- [ ] Acceso a recurso de otro usuario devuelve 403

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Acceso permitido con token válido
DADO que tengo token JWT válido
Y no está expirado
CUANDO accedo a GET /api/documents
ENTONCES el middleware valida el token
Y devuelve lista de documentos
Y recibo estado 200

Escenario: Acceso denegado - sin token
DADO que no envío token
CUANDO intento GET /api/documents
ENTONCES devuelve error 401

Escenario: Acceso denegado - token inválido
DADO que envío token malformado
CUANDO intento GET /api/documents
ENTONCES devuelve error 401

Escenario: Prohibición de acceso - recurso de otro usuario
DADO que pertenezco a usuario_A
Y existe documento de usuario_B
CUANDO intento acceder a documento de usuario_B
ENTONCES devuelve error 403
```"""
    },
    {
        "title": "Manejo robusto de errores y validaciones",
        "labels": ["user-story", "backend", "frontend"],
        "body": """**Como** usuario de la plataforma  
**Quiero** recibir mensajes de error claros y amigables  
**Para** entender qué salió mal y cómo puedo corregirlo

## Criterios de Aceptación

- [ ] Todos los errores tienen mensajes claros en español
- [ ] Errores de validación listan campos específicos
- [ ] Errores de servicio externo muestran fallback amigable
- [ ] No se exponen detalles técnicos al usuario
- [ ] Se loguea el error completo en servidor
- [ ] Timeout de respuestas se maneja gracefully

## Escenarios de Prueba (Gherkin)

```gherkin
Escenario: Error de validación - campos requeridos
DADO que estoy en formulario de login
CUANDO intento enviar sin email
ENTONCES muestra error "El email es requerido"
Y destaca el campo faltante

Escenario: Error de API externa - Gemini no disponible
DADO que hago una pregunta
CUANDO API de Gemini está no disponible
ENTONCES muestra "No se pudo completar la respuesta. Intenta de nuevo"
Y loguea error completo

Escenario: Timeout de carga larga
DADO que subo PDF muy grande
Y timeout es 30 segundos
CUANDO pasan 30 segundos
ENTONCES interrumpe petición
Y muestra "La carga tardó demasiado"
```"""
    },
]

def create_labels(repo_owner, repo_name):
    """Crear labels predeterminados"""
    label_configs = [
        ("user-story", "0075ca", "User story con formato Como...Quiero...Para..."),
        ("backend", "d73a49", "Cambios en backend FastAPI"),
        ("frontend", "0366d6", "Cambios en frontend Next.js"),
        ("gherkin", "f1e6b5", "Escenarios en formato Gherkin"),
        ("acceptance-criteria", "c5def5", "Criterios de aceptación definidos"),
    ]
    
    for label_name, color, description in label_configs:
        try:
            cmd = [
                "gh", "label", "create", label_name,
                f"--repo={repo_owner}/{repo_name}",
                f"--color={color}",
                f"--description={description}",
                "--force"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Label '{label_name}' creado")
            else:
                print(f"⚠ Label '{label_name}' (puede que ya exista)")
        except Exception as e:
            print(f"✗ Error creando label '{label_name}': {e}")

def create_issues(repo_owner, repo_name, issues_list):
    """Crear issues en GitHub"""
    created_count = 0
    failed_count = 0
    
    for idx, issue in enumerate(issues_list, 1):
        try:
            cmd = [
                "gh", "issue", "create",
                f"--repo={repo_owner}/{repo_name}",
                f"--title={issue['title']}",
                f"--body={issue['body']}",
            ]
            
            print(f"\n[{idx}/{len(issues_list)}] Creando: {issue['title']}...", end=" ")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Extrae el número de issue del URL
                issue_url = result.stdout.strip()
                print(f"✓ Creado")
                print(f"    URL: {issue_url}")
                created_count += 1
            else:
                print(f"✗ Error")
                print(f"    {result.stderr.strip()}")
                failed_count += 1
                
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout")
            failed_count += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"Resumen: {created_count} creados, {failed_count} fallidos")
    print(f"{'='*60}")

if __name__ == "__main__":
    print(f"🚀 Creando issues en {REPO_OWNER}/{REPO_NAME}\n")
    
    print("Creando labels...")
    create_labels(REPO_OWNER, REPO_NAME)
    
    print("\nCreando issues...")
    create_issues(REPO_OWNER, REPO_NAME, issues)
