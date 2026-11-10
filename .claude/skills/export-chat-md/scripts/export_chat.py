#!/usr/bin/env python3
"""Exporta la transcripción de Claude Code (JSONL) a Markdown listo para GitHub.

Uso: python -I export_chat.py [ruta.jsonl] [salida.md]
Sin argumentos: toma la transcripción más reciente del proyecto actual.
"""
import json, sys, os, glob
from pathlib import Path

def find_latest():
    base = Path.home() / ".claude" / "projects"
    cwd_key = str(Path.cwd()).replace(":", "-").replace("\\", "-").replace("/", "-").replace(" ", "-")
    cands = glob.glob(str(base / "*" / "*.jsonl"))
    exact = [c for c in cands if Path(c).parent.name.lower() == cwd_key.lower()]
    pool = exact or cands
    return max(pool, key=os.path.getmtime)

def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for b in content:
        t = b.get("type")
        if t == "text":
            out.append(b["text"])
        elif t == "tool_use":
            inp = json.dumps(b.get("input", {}), ensure_ascii=False)
            out.append(f"> 🔧 *Herramienta:* `{b.get('name')}` — `{inp[:300]}`")
        elif t == "image":
            out.append("*[imagen adjunta]*")
        # tool_result y thinking se omiten por brevedad/privacidad
    return "\n\n".join(out)

def main():
    src = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else find_latest()
    dst = sys.argv[2] if len(sys.argv) > 2 else "conversacion.md"
    lines = ["# Conversación exportada", f"\n_Fuente: `{Path(src).name}`_\n"]
    with open(src, encoding="utf-8") as f:
        for raw in f:
            try:
                e = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if e.get("type") not in ("user", "assistant") or e.get("isMeta"):
                continue
            msg = e.get("message", {})
            body = text_of(msg.get("content", "")).strip()
            if not body or "<system-reminder>" in body[:50]:
                continue
            who = "👤 Usuario" if e["type"] == "user" else "🤖 Claude"
            lines.append(f"\n---\n\n## {who}\n\n{body}\n")
    import re
    out = "\n".join(lines)
    out = out.replace(Path.home().name, "<usuario>")                       # usuario de Windows en rutas
    out = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<correo-omitido>", out)      # correos
    Path(dst).write_text(out, encoding="utf-8")
    print(f"Exportado: {dst}")

if __name__ == "__main__":
    main()
