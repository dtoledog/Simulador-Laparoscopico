# Cómo subir este proyecto a GitHub

Guía paso a paso (Windows, PowerShell). Sustituye lo que está entre `<...>` por tus datos.

## 0. Requisitos
- Cuenta en [github.com](https://github.com).
- Git instalado. Comprueba con `git --version`. Si no está: `winget install --id Git.Git -e`, y luego cierra y abre la terminal.
- (Opcional) GitHub CLI: `winget install --id GitHub.cli -e`.

## 1. Qué se sube y qué no
Carpeta del proyecto: `Proyecto IA 3d`

| Carpeta / archivo | ¿Subir? | Nota |
|---|---|---|
| `cad/simulator.py`, `cad/simulator.scad` | Sí | Código fuente del modelo. |
| `cad/out/*.step` | Sí | Para importar en Onshape. |
| `cad/out/*.stl` | Sí | Pesan algo más; si el repo crece mucho, usa Git LFS o súbelos como *Release*. |
| `cad/out/report.json` | Sí | Resultado de la validación. |
| `docs/` | Sí | Entrega técnica y esta guía. `docs/conversacion.md` (si lo generas) **no se sube**: está en `.gitignore`. |
| `.claude/skills/` | Sí | Las skills del proyecto. |
| `.claude/settings*.json` | **No** | Pueden tener configuración personal. |
| Imágenes de referencia de terceros | **Revisar** | Puede tener derechos de autor (marca de agua visible). Mejor no subirla. |

## 2. Crear el `.gitignore`
Crea un archivo `.gitignore` en la raíz con este contenido:

```
__pycache__/
*.pyc
.claude/settings.json
.claude/settings.local.json
*.tmp
```

## 3. Inicializar el repositorio local
```powershell
git init -b main
git config user.name "<tu nombre>"
git config user.email "<correo de tu cuenta de GitHub o el correo noreply>"
git add README.md LICENSE .gitignore cad/simulator.py cad/simulator.scad cad/out docs .claude/skills
git status
```
Revisa que `git status` solo liste lo que quieres subir.

> **Privacidad del correo:** puedes usar el correo `noreply` que GitHub te da en *Settings → Emails* para que tu correo real no quede en el historial de commits.

## 4. Primer commit
```powershell
git commit -m "Simulador laparoscopico de bajo costo: modelo CadQuery, STEP/STL, documentacion"
```

## 5. Crear el repositorio en GitHub y subirlo

### Opción A: con GitHub CLI
```powershell
gh auth login
gh repo create <nombre-del-repo> --private --source . --remote origin --push
```
Usa `--public` si quieres que sea visible para todos.

### Opción B: desde la web
1. En GitHub: **New repository**. Nombre sugerido: `simulador-laparoscopico-lowcost`.
2. Elige **Private** o **Public**. **No** marques "Add a README" ni ".gitignore" (ya los tienes).
3. Pulsa **Create repository** y copia la URL HTTPS.
4. En la terminal:
```powershell
git remote add origin https://github.com/<tu-usuario>/<nombre-del-repo>.git
git push -u origin main
```
Si te pide credenciales, usa tu usuario y un **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens), no tu contraseña.

## 6. Añadir un README
Crea `README.md` en la raíz con lo esencial:

```markdown
# Simulador laparoscópico de bajo costo (réplica tipo LE-1100)
Modelo paramétrico (CadQuery) de un entrenador laparoscópico torso con piernas, para impresión 3D y visualización en Onshape.

- Documento técnico: docs/ENTREGA_SIMULADOR_LE1100.md
- Generar el modelo: `pip install cadquery` y `python cad/simulator.py`
- Abrir en Onshape: importar los .step de `cad/out/` (ver sección 3 del documento técnico)
- Estado: modelo validado geométricamente; no probado físicamente. No es un dispositivo médico.
```

Luego:
```powershell
git add README.md
git commit -m "Agrega README"
git push
```

## 7. Actualizar el repositorio más adelante
```powershell
git add <archivos cambiados>
git commit -m "Descripcion del cambio"
git push
```

## 8. Archivos grandes (opcional)
Si GitHub rechaza archivos de más de 100 MB o el repo se vuelve pesado:
```powershell
git lfs install
git lfs track "*.stl"
git add .gitattributes
```
Haz esto **antes** de añadir los `.stl`.

## 9. Lista de comprobación final
- [ ] `git status` no lista `docs/conversacion.md`.
- [ ] No se subieron `.claude/settings*.json`.
- [ ] Imagen de referencia de terceros fuera del repo (o con permiso).
- [ ] Repositorio en **Private** hasta que la revises, si tienes dudas.
- [ ] Citas marcadas como no verificadas siguen marcadas en la documentación.
