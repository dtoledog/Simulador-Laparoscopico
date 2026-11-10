# Réplica funcional de bajo costo de simulador laparoscópico tipo LE-1100 (torso con piernas)

Documento técnico · Ingeniería biomédica / diseño industrial · Generado el 2026-11-10
Archivos CAD: `cad/simulator.py` (STEP/STL, **validado**), `cad/simulator.scad` (**no ejecutado**), salidas en `cad/out/`.

> **Aviso de alcance.** Es un entrenador de habilidades psicomotoras de bajo costo, **no** un dispositivo médico certificado y **no** una validación de FLS. Todo valor numérico marcado como *[diseño propio]* es una decisión de diseño y no una cita.

---

## 0. Auditoría de fuentes (hecha antes de diseñar)

Cada cifra del prompt se buscó en la web. Resultado:

| Afirmación del prompt | Estado | Qué se hizo |
|---|---|---|
| FLS: caja 12×6×6 in, cubierta a 15° | **NO verificada**. La búsqueda y la guía de usuario del FLS (Limbs & Things) no dieron esas cifras. El PDF de la guía no se pudo leer (flujo comprimido). | Se usan como **parámetros de diseño propios** (15° = parámetro `A`). |
| Instrumental de 330 mm | **Contradicha en parte**: las fuentes secundarias dan 36 cm como longitud estándar del instrumental laparoscópico adulto (45 cm para pacientes obesos) y 28 cm en pediatría. 330 mm no aparece. | Se usa **solo como longitud útil de entrenamiento** *[diseño propio]*. El trayecto puerto→blanco del diseño es 118 mm, muy dentro de cualquiera de esas longitudes. |
| Ángulo de manipulación 45–60° | **Confirmado** por fuentes secundarias (capítulo Springer y revisiones). Ángulos <45° o >75° empeoran el desempeño. | Diseño con **55.8°** calculado (ver §2). |
| Arco de trocares a 15–20 cm del blanco, 5–7 cm entre trocares | Aparece en una tabla ergonómica de una fuente secundaria; **no es del FLS**. | Se usa como orientación. El simulador es compacto (puertos a 55–80 mm). |
| **InVeSo** | **No se encontró ninguna fuente.** No se puede confirmar qué es, quién lo hizo ni si es de hardware abierto. | **Eliminado como pilar.** No se cita. Si tienes la referencia exacta, dímela y la verifico. |
| **EOsim** | **Existe, pero es el producto comercial *eoSim*** (distribuido por Limbs & Things), no un proyecto de hardware abierto. Tiene estudios de validación publicados. | Se cita **solo como referencia comercial** de simulador portátil de bajo costo, no como diseño abierto. |
| "IEEE Transactions on Medical Robotics" | No apareció ningún estudio pertinente de simuladores laparoscópicos de caja en esa revista. | **No se cita.** |

**Consecuencia:** el diseño ya no depende de FLS/InVeSo como fundamento cuantitativo. Se apoya en (i) el ángulo de manipulación 45–60°, que sí está respaldado, (ii) la revisión sistemática de simuladores de bajo costo y (iii) la estructura de simuladores validados (eoSim, FLS) como referencia de qué tareas debe permitir.

---

## 1. Análisis de la imagen de referencia

Características a replicar, con las diferencias entre la imagen y el prompt resueltas según tus decisiones:

| Elemento en la imagen | Decisión en la réplica |
|---|---|
| Carcasa blanca brillante, aspecto limpio | Carcasa blanca impresa en PLA, con lijado y pintura opcionales. |
| Forma: arco/silla con dos "patas" redondeadas | **Decisión tuya: torso con piernas.** Torso de 340×205 mm en planta y dos piernas de 150×200 mm, con esquinas de radio 15 mm. |
| Puerto central elevado | Cuello cilíndrico OD 66 / ID 52 mm, 35 mm sobre la cubierta, con pestaña. Va en el centro (0, 140). |
| Collar del puerto: **negro** en la imagen (el prompt decía azul) | **Decisión tuya: el color de menor costo → negro.** Es el color básico estándar de PLA, sin sobreprecio frente al blanco, y no necesita pintura. Pesa ~30 g (≈ $0.65). *[Los precios por color varían según tienda; no verifiqué un catálogo]*. |
| 3 puertos laterales con anillo | 3 guías de trocar (izquierda, derecha y asistente) en configuración en abanico. |
| Pantalla táctil y botón "LE-1100" en la pierna derecha | **Decisión tuya: pantalla externa.** No hay pantalla a bordo. El panel frontal tiene un orificio para **botón Ø12**, un **USB-C panel-mount** y un **HDMI panel-mount** opcional. Se conecta a monitor, tablet o smartphone (ver §2.4). |
| Texto "LE-1100" | Es la marca/modelo del producto original. En la réplica se deja una etiqueta propia, sin copiar la marca. |

---

## 2. Especificaciones técnicas y diseño

### 2.1 Dimensiones *[diseño propio]*
| Parámetro | Valor |
|---|---|
| Huella total | 340 × 405 mm (torso 340×205 + piernas 200) |
| Altura de cubierta | 90 mm en y=0 → 144.9 mm en el extremo del torso (ángulo **15°**, parámetro `A`) |
| Piernas | 2 × (150 × 200 × 90 mm), cubierta plana |
| Pared impresa | 2.5 mm |
| Segmentación | 5 baldosas (torso izq/centro/der + pierna izq/der) para caber en cama de 220 mm |

### 2.2 Triangulación y puertos
Ángulo entre los ejes de los dos trocares principales hacia un blanco a 15 mm sobre el piso, calculado en el script: **55.8°** (objetivo 45–60°, respaldado por fuentes secundarias). Trayecto puerto→blanco: **117.6 mm**.

| Puerto | Posición (x, y) mm | Nota |
|---|---|---|
| Cámara | (0, 140) | Cuello elevado + collar negro |
| Trocar izq. | (−55, 60) | |
| Trocar der. | (55, 60) | |
| Asistente | (135, 135) | En la baldosa derecha |

Guía de trocar: **ID 11.5 mm** (para trocares de 10–11 mm), OD 20, pestaña Ø34 con 2 tornillos M3. Si los trocares tienen otro diámetro, cambia `TROC_ID` en `cad/simulator.py`.

### 2.3 Componentes
- **Iluminación:** tira LED COB 6000 K, 12 V, pegada bajo la cubierta.
- **Cámara:** webcam USB 1080p con enfoque manual. FOV 90° y distancia de enfoque de 18 cm son **requisitos tuyos, no verificados contra un modelo comercial**: elige el modelo y comprueba que enfoque a 12–18 cm. El soporte (`webcam_brazo` + `webcam_cuna`) tiene **3 ejes**: giro (ranuras ±20°), cabeceo (tornillo M4) y ancho de cuna ajustable (`cam_w`). **Verificar el ajuste con la webcam real.**
- **Estructura:** placa base MDF/acrílico de 4 mm, 10 tornillos M3 a bosses internos y conectores esquineros de 90° para la bandeja de módulos.
- **Módulos de entrenamiento:** pad de sutura, peg transfer, etc. sobre la placa base.

### 2.4 Pantalla: conexión por USB-C o HDMI
La webcam es un dispositivo **UVC** (cámara USB estándar). Rutas de visualización:

| Ruta | Cómo | Costo extra |
|---|---|---|
| **A. USB-C → PC / smartphone / tablet** (recomendada) | Cable USB-C desde el panel frontal al equipo. Se ve con la app de cámara del PC o una app UVC en Android. En iPhone/iPad con USB-C, el soporte UVC depende de la versión de iPadOS/iOS. **Compatibilidad a comprobar con tu dispositivo.** | $0 (cable incluido en BOM) |
| **B. HDMI → monitor/TV** | Una webcam no emite HDMI. Hace falta un **puente**: un Raspberry Pi Zero 2 W (o mini-PC) que reciba el UVC y saque HDMI. El panel tiene el orificio para el HDMI. | ≈ +$20–25, **fuera del presupuesto base** |

---

## 3. Modelado 3D paramétrico

**Se ejecutó y se validó** `cad/simulator.py` (CadQuery 2.8.0). Resultado: las 12 piezas son sólidos únicos y válidos; las 5 baldosas caben en la cama de 220 mm.

Módulos pedidos:
- **a)** `camera_neck()` + `collar()`: cuello elevado detallado con collar negro.
- **b)** `trocar_guide()`: guía con pestaña de sujeción.
- **c)** `corner_connector()`: conector esquinero a 90°, 3 ranuras para paneles de 4 mm.
- **d)** `webcam_arm()` + `webcam_cradle()`: soporte multieje.
- **e)** `build_shell()` + `build_tiles()`: carcasa anatómica segmentada en 5 baldosas con pestañas de unión M3, y `base_plate()` para la placa base.

**Qué NO se verificó:** la carcasa no se inspeccionó visualmente en un visor 3D. Se validaron la validez geométrica, los sólidos únicos y los tamaños. Al importarla en Onshape, revisa el aspecto, los cortes de los puertos y los tornillos. El `.scad` es una traducción **sin ejecutar** (no hay OpenSCAD instalado).

### Cómo verla en Onshape
Onshape **no ejecuta OpenSCAD ni Python**. La ruta es importar los STEP:
1. Entra en onshape.com → **Create → Document**. *En cuentas gratuitas los documentos son públicos.*
2. Pestaña **+ → Import** y selecciona los archivos de `cad/out/`.
3. Para ver el conjunto: importa `ensamble_LE1100.step` (colores: blanco, collar negro, placa base en madera). Para editar piezas: importa los `*.step` sueltos.
4. Unidades: mm. Los `.stl` sirven para laminar, pero en Onshape llegan como malla no editable.
5. Para cambiar parámetros: edita las variables al inicio de `cad/simulator.py`, ejecuta `python cad/simulator.py` y reimporta.

Resultados de la validación (de `cad/out/report.json`):

| Pieza | Sólidos | Tamaño (mm) | PLA (g) |
|---|---|---|---|
| Baldosa torso izq. | 1 | 70×205×145 | 159 |
| Baldosa torso centro | 1 | 200×205×145 | 226 |
| Baldosa torso der. | 1 | 70×205×145 | 158 |
| Pierna izq. / der. | 1 / 1 | 150×200×90 | 246 / 245 |
| Guía de trocar (×3) | 1 | 34×34×28 | 9.4 c/u |
| Cuello de cámara | 1 | 94×94×43 | 77 |
| Collar (negro) | 1 | 76×76×8 | 30 |
| Brazo / cuna webcam | 1 / 1 | 65×65×94 / 72×26×44 | 16 / 21 |
| Conector esquinero (×4) | 1 | 26×26×26 | 15.5 c/u |
| Placa base (4 mm, MDF) | 1 | 340×405×4 | — |

**Impresión:** piernas con la cubierta contra la cama, sin soportes. Torso con la base abierta hacia abajo y soportes bajo la cubierta inclinada (con la cubierta sobre la cama la baldosa mide 235 mm y no cabe). Estimación gruesa: 80–120 h de impresión en total *[estimación mía, no medida]*.

---

## 4. Lista de materiales (BOM)

| Categoría | Componente | Especificación técnica | Cant. | Tipo |
|---|---|---|---|---|
| Estructura | Carcasa (5 baldosas) | PLA blanco, pared 2.5 mm | ≈1034 g | Impreso 3D |
| Estructura | Guías de trocar | ID 11.5 mm, pestaña M3 | 3 | Impreso 3D |
| Estructura | Cuello de cámara | OD 66 / ID 52 mm | 1 | Impreso 3D |
| Estructura | Collar | PLA **negro**, OD 76 | 1 | Impreso 3D |
| Estructura | Conectores esquineros 90° | Ranura 4.2 mm | 4 | Impreso 3D |
| Estructura | Placa base | MDF/acrílico 4 mm, 340×405 mm | 1 | Comercial (corte láser/CNC; DXF en `cad/out/placa_base_4mm.dxf`) |
| Estructura | Paneles de bandeja | MDF 4 mm, retales | 3–4 | Comercial/Reciclado |
| Óptica | Webcam USB | 1080p, FOV ~90°, enfoque manual | 1 | Comercial |
| Óptica | Soporte webcam | Brazo + cuna, M4 | 1 | Impreso 3D |
| Iluminación | Tira LED COB | 6000 K, 12 V, ~1 m | 1 | Comercial |
| Alimentación | Fuente | 12 V, 1–2 A | 1 | Comercial |
| Interfaz | Panel USB-C | Extensión panel-mount hembra-hembra | 1 | Comercial |
| Interfaz | Panel HDMI (opcional) | Extensión panel-mount | 0–1 | Comercial |
| Interfaz | Pulsador | Ø12 mm con LED | 1 | Comercial |
| Interfaz | Cable USB-C | 1.5 m | 1 | Comercial |
| Pantalla | Monitor / tablet / smartphone | Propio del usuario | 1 | Reciclado |
| Tornillería | M3×10 + tuercas (guías, cuello) | | 10 | Comercial |
| Tornillería | M3×14 + tuercas (uniones) | 8 pares de pestañas | 8 | Comercial |
| Tornillería | M3×16 (base) | A bosses con piloto Ø2.5 | 10 | Comercial |
| Tornillería | M3×20 (collar + placa) | | 3 | Comercial |
| Tornillería | M4×20 + tuerca | Eje de cabeceo | 1 | Comercial |
| Cableado | Pasacables de goma | | 2 | Comercial |
| Entrenamiento | Pad de sutura | Silicona/espuma | 1 | Comercial |
| Entrenamiento | Peg transfer | Pegs impresos + tablero | 1 set | Impreso 3D |

---

## 5. Desglose de costos (USD, estimación)

Precios **típicos de mercado (Amazon/AliExpress)**, estimados, **no consultados en tienda en tiempo real**. Impresión a $0.02/g con 10 % de desperdicio.

| Elemento | Precio unit. (USD) | Cant. | Total (USD) |
|---|---|---|---|
| PLA blanco (carcasa + piezas: 1238 g × 1.10) | 0.02 /g | 1362 g | 27.2 |
| PLA negro (collar: 30 g × 1.10) | 0.02 /g | 33 g | 0.7 |
| PLA pegs peg transfer | 0.02 /g | 30 g | 0.6 |
| Webcam USB 1080p enfoque manual | 15.0 | 1 | 15.0 |
| Tira LED COB 12 V, 1 m | 4.0 | 1 | 4.0 |
| Fuente 12 V | 5.0 | 1 | 5.0 |
| Placa base MDF 4 mm | 4.0 | 1 | 4.0 |
| Paneles MDF de bandeja | 2.0 | 1 | 2.0 |
| Kit tornillería M3/M4 | 4.0 | 1 | 4.0 |
| Pasacables de goma | 2.0 | 1 | 2.0 |
| Pad de sutura | 5.0 | 1 | 5.0 |
| USB-C panel-mount | 4.0 | 1 | 4.0 |
| Pulsador Ø12 mm | 1.5 | 1 | 1.5 |
| Cable USB-C 1.5 m | 3.0 | 1 | 3.0 |
| **TOTAL base (ruta A, USB-C)** | | | **≈ 78.0** |

**El total supera el objetivo de $75 en unos $3.** Opciones para cumplirlo:
- Sustituir la fuente de 12 V (−$5) por una tira LED de 5 V alimentada desde el mismo USB (≈ +$1): total ≈ **$74**.
- Imprimir con pared de 2.0 mm: ahorra ~15–20 % del filamento.

La ruta HDMI (Raspberry Pi Zero 2 W + cable + microSD) suma ≈ **$20–25** y queda fuera del objetivo.

---

## 6. Guía rápida de ensamble

1. **Impresión 3D.** Baldosas de piernas con la cubierta contra la cama, sin soportes. Baldosas de torso con la base abierta hacia abajo y soportes bajo la cubierta. Collar en negro, resto en blanco. Piezas pequeñas en PLA o PETG.
2. **Corte de paneles.** Placa base de 340×405 mm en MDF o acrílico de 4 mm, con 10 agujeros Ø3.2 (posiciones en `BOSSES`) y pasacables. Paneles de bandeja con retales. El contorno 2D listo para corte está en `cad/out/placa_base_4mm.dxf` (unidades mm; comprueba la escala en tu software de corte).
3. **Chasis.** Une las baldosas con tornillos M3×14 y tuerca en las pestañas de las costuras (x = ±100 mm entre baldosas de torso; y = 0 entre piernas y torso). Fija el conjunto a la placa base con los 10 tornillos M3×16 a los bosses. Monta los conectores esquineros y los paneles de la bandeja.
4. **Electrónica.** Pega la tira LED COB bajo la cubierta, lejos del campo de visión. Instala el pulsador Ø12 y el USB-C panel-mount en la cara frontal de la pierna derecha. Fija el cuello con 4 M3×10 y sus tuercas. Atornilla el brazo de la webcam bajo el collar con 3 M3×20 y monta la webcam en la cuna. Conecta el cable USB desde la webcam al panel y la fuente al LED.
5. **Ensamble final.** Instala las 3 guías de trocar con 2 M3×10 cada una. Coloca el pad de sutura y los pegs en la bandeja. Ajusta el enfoque manual a 12–18 cm y el cabeceo con el M4. Verifica con instrumental real: ángulo de manipulación, campo visual y holguras. **Registra cualquier ajuste necesario: la carcasa no se ha probado físicamente.**

---

## 7. Referencias

### Verificadas (existencia confirmada por búsqueda; datos bibliográficos finos por completar)
1. Li MM, George J. *A systematic review of low-cost laparoscopic simulators.* **Surgical Endoscopy**, 2016/2017. Revisión; costos £3–£216 (no comerciales) y £60–£1007 (comerciales); componentes comunes: cavidad abdominal, puertos, luz, visualización, monitor. PMC5216104. *[verificar volumen y páginas]*
2. Hennessey IA, Hewett P. *Construct, concurrent, and content validity of the eoSim laparoscopic simulator.* 2013. 47 participantes; correlación con FLS 0.78 según el resumen consultado. *[verificar revista, volumen y páginas]*
3. Leijte E, et al. Estudio de validez facial, de contenido y de constructo de **eoSim** (sutura avanzada y transferencia de aguja, 104 participantes). **Surgical Endoscopy**, 2019. DOI 10.1007/s00464-018-06652-3. *[verificar título exacto]*
4. *A Novel Do-It-Yourself Approach to Simulating Minimally Invasive Laparoscopic Surgery.* **Cureus**, 2023. PMC10241665.
5. *Development and Validation of a Homemade, Low-Cost Laparoscopic Simulator for Resident Surgeons (LABOT).* 2020. *[verificar revista]*
6. Limbs & Things. *FLS Trainer Box – User Guide* (producto/manual comercial del FLS). Consultado; **no se pudieron leer las cifras de dimensiones**.
7. Capítulo Springer (doi:10.1007/978-981-19-3755-2_6) y fuentes de laparoscopyhospital.com para el ángulo de manipulación de 45–60° (**fuentes secundarias**, no normativas).


 **Precios de la sección 5**: estimaciones típicas, sin consulta de tienda.
