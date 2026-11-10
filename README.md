# Simulador laparoscópico de bajo costo (réplica funcional tipo LE-1100)

Diseño paramétrico de un entrenador laparoscópico de caja con forma de **torso con piernas**, pensado para impresión 3D (PLA) y visualización en [Onshape](https://www.onshape.com/es). Incluye modelo CAD, lista de materiales, costos y guía de ensamble.

> ⚠️ **Estado: prototipo no probado físicamente.**
> - El modelo se validó **geométricamente** (sólidos válidos, tamaños, ángulo de manipulación calculado), pero **nadie lo ha impreso ni ensamblado**. Pueden aparecer errores de ajuste en las uniones M3, la webcam, el panel frontal o las guías de trocar.
> - No se ha inspeccionado visualmente en un visor 3D antes de publicarlo: revísalo al importarlo.
> - Es un **entrenador de habilidades psicomotoras, no un dispositivo médico** y no ha sido validado clínicamente (ni FLS ni otro programa).
> - Varias cifras de diseño (cubierta a 15°, instrumental de 330 mm, dimensiones tipo FLS) son **parámetros propios no confirmados en fuente primaria**. Ver la auditoría de fuentes en el documento técnico.

## Contenido
| Ruta | Qué es |
|---|---|
| [docs/ENTREGA_SIMULADOR_LE1100.md](docs/ENTREGA_SIMULADOR_LE1100.md) | Documento técnico: auditoría de fuentes, especificaciones, BOM, costos, guía de ensamble y referencias |
| [cad/simulator.py](cad/simulator.py) | Modelo paramétrico en **CadQuery** (validado). Genera STEP/STL/DXF |
| [cad/simulator.scad](cad/simulator.scad) | Equivalente en OpenSCAD (**no ejecutado**) |
| `cad/out/*.step` | Piezas y ensamble para importar en Onshape (editables) |
| `cad/out/*.stl` | Mallas para el laminador de impresión |
| `cad/out/placa_base_4mm.dxf` | Contorno 2D de la placa base MDF/acrílico 4 mm (corte láser/CNC) |
| `cad/out/report.json` | Resultados de validación (validez, tamaños, masa de PLA, ángulo) |
| [docs/SUBIR_A_GITHUB.md](docs/SUBIR_A_GITHUB.md) | Guía para publicar el repositorio |
| `.claude/skills/` | Skills usadas para generar el diseño |

## Cómo abrirlo en Onshape
1. Entra en onshape.com → **Create → Document**. *(En el plan gratuito los documentos son públicos.)*
2. Pestaña **+ → Import** y selecciona los `.step` de `cad/out/`.
3. Para ver todo: `ensamble_LE1100.step`. Para editar o imprimir una pieza: el `.step` suelto.
4. Unidades: milímetros. Los `.stl` son para el laminador, en Onshape llegan como malla no editable.

## Regenerar el modelo
Requisitos: Python 3.10+ y [CadQuery](https://github.com/CadQuery/cadquery).
```bash
pip install cadquery
python cad/simulator.py
```
Los parámetros están al inicio de `cad/simulator.py` (`A`, `PORTS`, `TROC_ID`, `WALL`, …). Verificado con CadQuery 2.8.0 y Python 3.14.

## Resumen del diseño
- Huella 340 × 405 mm; cubierta inclinada 15° (parámetro) de 90 a 145 mm de altura; pared 2.5 mm.
- 5 baldosas impresas (torso ×3, piernas ×2) que caben en una cama de 220 mm, con pestañas de unión M3.
- Puerto de cámara central elevado con collar negro; 3 guías de trocar (ID 11.5 mm) en abanico; ángulo de manipulación calculado **55.8°**.
- Webcam USB 1080p con soporte de 3 ejes; iluminación LED COB 6000 K.
- Visualización por **USB-C** a PC/tablet/smartphone (UVC). HDMI requiere un puente (p. ej. Raspberry Pi), no incluido.
- Costo estimado **≈ $78 USD** (≈ $74 con LED de 5 V). Precios típicos, no consultados en tienda.

## Limitaciones conocidas
- Cortes del panel frontal (botón Ø12, USB-C, HDMI) y cuna de la webcam son genéricos: **verificar con las piezas reales**.
- El torso se imprime con base abierta hacia abajo y soportes bajo la cubierta inclinada; la estimación de 80–120 h de impresión es aproximada.
- Referencias bibliográficas: algunas marcadas `[verificar]` (volumen/páginas). **InVeSo no pudo localizarse**; eoSim es un producto comercial.

## Contribuir
Si lo imprimes o lo pruebas, abre un *issue* con fotos y los ajustes que necesitaste: es la información que más falta.

## Licencia
Sin licencia explícita: por defecto, todos los derechos quedan reservados al autor. Otras personas pueden ver y bifurcar el repositorio en GitHub, pero no tienen permiso legal para reutilizarlo ni redistribuirlo sin autorización.
