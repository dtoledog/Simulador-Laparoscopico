---
name: onshape-sim-design
description: Diseña un simulador/entrenador laparoscópico de bajo costo (o hardware médico similar) y entrega modelo 3D paramétrico visualizable en Onshape, BOM, costos y guía de ensamble. Usar cuando se pida replicar un simulador desde una imagen, generar CAD (CadQuery/OpenSCAD/STEP/STL) para Onshape, o el prompt de 7 secciones de simulador laparoscópico.
---

# Skill: onshape-sim-design

## Principio clave
Onshape NO ejecuta OpenSCAD ni Python. Rutas válidas (por orden):
1. **CadQuery (Python) → STEP**: B-rep real; se importa como piezas editables. RUTA PRINCIPAL. Instalar con `pip install cadquery` (probado con 2.8.0, Python 3.14).
2. **OpenSCAD → STL**: solo malla (sin features). Útil para laminar. Marcar "NO EJECUTADO" si OpenSCAD no está instalado.
3. **FeatureScript**: solo si se pide parametría nativa de Onshape.
Importación: Documento → `+` → Import → archivos `.step` de `cad/out/` (ensamble: `ensamble_*.step`). Unidades mm. Las cuentas gratuitas crean documentos públicos: avisar antes de subir.

## Flujo
1. Auditar imagen y prompt (ver verificaciones) y listar discrepancias antes de generar. Preguntar solo decisiones que cambian el diseño.
2. Congelar parámetros en un bloque único al inicio del script.
3. Segmentar la carcasa en baldosas que quepan en la cama (por defecto 220 mm) con pestañas M3 en las costuras. Comprobar la orientación de impresión: una cubierta inclinada puede no caber boca abajo; en ese caso imprimir con la base abierta hacia abajo y soportes.
4. Generar `cad/simulator.py` (CadQuery; exporta STEP+STL por pieza + ensamble con colores + `report.json`) y `cad/simulator.scad` (mismos parámetros).
5. Validar: ejecutar el script y comprobar `isValid()`, número de sólidos (=1), bbox y que cabe en cama. Peso de PLA = volumen × 1.24 g/cm³. No afirmar que "funciona" lo que no se ejecutó. Piezas sin inspeccionar visualmente: decirlo.
6. Entregar las 7 secciones del prompt en `docs/` + rutas a STEP/STL + pasos de importación a Onshape.

## Verificaciones obligatorias (anti-alucinación)
- **Citas**: verificar cada referencia con WebSearch/WebFetch. No inventar autores, años, DOIs ni cifras. Separar "verificadas", "no verificadas" y "parámetro de diseño propio". Si una fuente pedida no existe (p. ej. InVeSo no se localizó; eoSim es producto comercial), eliminarla como pilar y decirlo.
- **Cifras clínicas**: el ángulo de manipulación 45–60° está respaldado por fuentes secundarias; 15° de cubierta, caja 12×6×6 in y 330 mm NO se confirmaron (el estándar encontrado es 36 cm).
- **Imagen vs prompt**: en la imagen el collar es negro y la carcasa es un arco con patas; confirmar con el usuario qué prevalece.
- **Precios**: son estimaciones; decir si el total supera el objetivo y proponer recortes.
- **Pantalla**: una webcam es UVC, no emite HDMI; un monitor HDMI requiere un puente (SBC). USB-C a PC/tablet/teléfono depende de la compatibilidad UVC del dispositivo.
- Es un entrenador, no un dispositivo médico certificado.

## Formato
Tablas Markdown (BOM y costos con las columnas del prompt), costo de impresión a 0.02 USD/g más 10 % de desperdicio, español.
