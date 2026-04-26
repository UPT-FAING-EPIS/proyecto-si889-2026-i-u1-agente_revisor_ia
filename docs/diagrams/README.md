# Diagramas UML (PlantUML)

Este directorio contiene los diagramas PlantUML generados para el proyecto "Agente Revisor IA".

Archivos incluidos:
- `diagrama_paquetes.puml` — Diagrama de paquetes del sistema.
- `diagrama_casos_uso.puml` — Diagrama de casos de uso.
- `diagrama_secuencia_revision_automatica.puml` — Secuencia simplificada de revisión automática.
- `diagrama_clases.puml` — Diagrama de clases simplificado.
- `diagrama_actividad_actual.puml` — Actividad del proceso actual (manual).
- `diagrama_actividad_propuesto.puml` — Actividad del proceso propuesto (automatizado).

Cómo renderizar:

- Usando la extensión PlantUML en VSCode (abrir el archivo `.puml` y usar vista previa).
- Usando PlantUML CLI:

```bash
java -jar plantuml.jar docs/diagrams/diagrama_paquetes.puml
```

- Usando PlantUML Server: https://www.plantuml.com/plantuml

Notas:
- Los diagramas son simplificaciones pensadas para documentación y validación con stakeholders.
- Ajustar etiquetas, niveles de detalle y relaciones según retroalimentación.
