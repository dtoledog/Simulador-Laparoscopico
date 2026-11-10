---
name: export-chat-md
description: Exporta la conversación actual de Claude Code a un archivo Markdown (texto) listo para subir a GitHub. Usar cuando el usuario diga "exporta la conversación", "guarda la ruta/chat en texto", "para GitHub" o similar.
---

# Skill: export-chat-md

1. Ejecutar desde la raíz del proyecto:
   `python -I .claude/skills/export-chat-md/scripts/export_chat.py "" docs/conversacion.md`
   (sin argumentos usa la transcripción más reciente de este proyecto; crear `docs/` si no existe).
2. Abrir el resultado y comprobar que no contiene datos privados (correo, rutas personales, claves). Si los hay, redactarlos o avisar al usuario antes de subir.
3. Las llamadas a herramientas se resumen y los resultados/razonamiento interno se omiten.
4. Sugerir al usuario: `git init`, `git add docs/ cad/ .claude/skills/`, commit y push (no ejecutarlo sin que lo pida).
