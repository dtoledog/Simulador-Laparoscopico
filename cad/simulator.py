"""
Simulador laparoscopico de bajo costo - torso con piernas (replica funcional tipo LE-1100)
CadQuery -> STEP (B-rep, editable) + STL.  Pensado para importarse en Onshape (unidades: mm).

Uso:  python cad/simulator.py      (genera cad/out/*.step, *.stl, report.json)

NOTA: todas las dimensiones son PARAMETROS DE DISENO PROPIOS (ver docs/ENTREGA...md, seccion 7).
Las cifras FLS/SAGES (15 deg, 330 mm, caja 12x6x6 in) NO pudieron verificarse en fuente primaria.
"""
import cadquery as cq
import math, json
from pathlib import Path

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ PARAMETROS
A       = 15.0            # inclinacion de cubierta (deg)  [parametro del prompt]
TA      = math.tan(math.radians(A))
W       = 340.0           # ancho del torso
L_T     = 205.0           # largo del torso (en planta). Limitado: L_T/cos(A) < cama 220
LEG_L   = 200.0           # largo de cada pierna
LEG_X0, LEG_X1 = 10.0, 160.0   # pierna entre x=10..160 (y espejo)
H0      = 90.0            # altura de cubierta en el borde de piernas / y=0
WALL    = 2.5             # espesor de pared impresa
FIL     = 15.0            # radio de esquinas en planta
BED     = 220.0           # cama de impresion util (mm)
SEAM_X  = 100.0           # costuras del torso en x=+-100
CAM_XY  = (0.0, 140.0)    # puerto de camara (centro)
PORTS   = [(-55.0, 60.0), (55.0, 60.0), (135.0, 135.0)]   # trocares: izq, der, asistente
PANEL_T = 4.0             # espesor MDF/acrilico
TROC_ID, TROC_OD, TROC_FL_OD = 11.5, 20.0, 34.0   # guia trocar
NECK_OD, NECK_ID, NECK_H = 66.0, 52.0, 35.0       # cuello puerto camara
NECK_FL_OD = 94.0
BC_RIM = 29.5            # circulo de pilotos M3 del borde del cuello
PLA_DENS = 1.24e-3        # g/mm3

def zdeck(y, t=0.0):
    return H0 + y * TA - t / math.cos(math.radians(A))

def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))

def cyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)

def on_deck(shape, x, y):
    """Coloca una pieza definida con +Z = normal de cubierta sobre la cubierta en (x,y)."""
    return shape.rotate((0, 0, 0), (1, 0, 0), A).translate((x, y, zdeck(y)))

def try_fillet(wp, sel, r):
    try:
        return wp.edges(sel).fillet(r)
    except Exception:
        return wp

# ------------------------------------------------------------------ CARCASA
def body(t):
    z0 = 0.0 if t == 0 else -1.0
    y0 = 0.0 if t == 0 else t
    y1 = L_T - t
    pts = [(y0, z0), (y1, z0), (y1, zdeck(y1, t)), (y0, zdeck(y0, t))]
    torso = cq.Workplane("YZ").polyline(pts).close().extrude(W / 2 - t, both=True)
    torso = try_fillet(torso.edges("|Z"), ">Y", FIL - t) if False else torso
    try:
        torso = torso.edges("|Z").edges(">Y").fillet(FIL - t)
    except Exception:
        pass
    parts = [torso]
    ytop = 1.0 if t == 0 else t + 1.0
    for sgn in (1, -1):
        xa, xb = sorted((sgn * (LEG_X0 + t), sgn * (LEG_X1 - t)))
        leg = box(xa, xb, -LEG_L + t, ytop, z0, H0 - t)
        try:
            leg = leg.edges("|Z").edges("<Y").fillet(FIL - t)
        except Exception:
            pass
        parts.append(leg)
    r = parts[0]
    for p in parts[1:]:
        r = r.union(p)
    return r

def build_shell():
    shell = body(0.0).cut(body(WALL))
    # perforaciones de puertos de trocar (Ø21) + 2 M3 por puerto
    for (x, y) in PORTS:
        shell = shell.cut(on_deck(cyl(10.5, -40, 20), x, y))
        for s in (-13, 13):
            shell = shell.cut(on_deck(cyl(1.7, -40, 20, x=s), x, y))
    # puerto de camara: agujero Ø75 + 4 M3 (BC Ø84)
    cx, cy = CAM_XY
    shell = shell.cut(on_deck(cyl(37.5, -40, 20), cx, cy))
    for k in range(4):
        a = math.radians(45 + 90 * k)
        shell = shell.cut(on_deck(cyl(1.7, -40, 20, x=42 * math.cos(a), y=42 * math.sin(a)), cx, cy))
    # panel frontal (pierna derecha, cara y=-LEG_L): boton Ø12, USB-C panel, HDMI panel  [VERIFICAR cortes con piezas reales]
    yf = -LEG_L
    shell = shell.cut(cq.Workplane("XZ").workplane(offset=-yf - 6).center(40, 45).circle(6.1).extrude(10))   # boton 12 mm
    shell = shell.cut(box(75 - 7, 75 + 7, yf - 1, yf + 6, 45 - 3.6, 45 + 3.6))                 # USB-C 14x7.2
    shell = shell.cut(box(115 - 8, 115 + 8, yf - 1, yf + 6, 45 - 3.8, 45 + 3.8))               # HDMI 16x7.6
    return shell

# ------------------------------------------------------------------ TILES + herrajes
BOSSES = {
    "torso_izq": [(-161.5, 60), (-161.5, 160)],
    "torso_cen": [(-40, 190.0), (40, 190.0)],
    "torso_der": [(161.5, 60), (161.5, 160)],
    "pierna_izq": [(-151.5, -60), (-151.5, -140)],
    "pierna_der": [(151.5, -60), (151.5, -140)],
}
# nota: el muro trasero interno del torso esta en y = L_T - WALL
BACK_Y = L_T - WALL - 6.5
BOSSES["torso_cen"] = [(-40, BACK_Y), (40, BACK_Y)]

def add_boss(tile, x, y):
    blk = box(x - 6.5, x + 6.5, y - 6.5, y + 6.5, 0, 14)
    pilot = cyl(1.25, 2, 15, x=x, y=y)
    return tile.union(blk).cut(pilot)

def add_tab(tile, cx, cy, cz, dx, dy, dz, axis):
    tile = tile.union(box(cx - dx / 2, cx + dx / 2, cy - dy / 2, cy + dy / 2, cz - dz / 2, cz + dz / 2))
    if axis == "x":
        h = cq.Workplane("YZ").center(cy, cz).circle(1.7).extrude(20, both=True).translate((cx, 0, 0))
    else:
        h = cq.Workplane("XZ").center(cx, cz).circle(1.7).extrude(20, both=True).translate((0, cy, 0))
    return tile.cut(h)

def build_tiles(shell):
    R = 400.0
    spec = {
        "torso_izq": box(-R, -SEAM_X, 0, R, -10, 400),
        "torso_cen": box(-SEAM_X, SEAM_X, 0, R, -10, 400),
        "torso_der": box(SEAM_X, R, 0, R, -10, 400),
        "pierna_izq": box(-R, 0, -R, 0, -10, 400),
        "pierna_der": box(0, R, -R, 0, -10, 400),
    }
    tiles = {k: shell.intersect(v) for k, v in spec.items()}
    for k in tiles:
        for (x, y) in BOSSES[k]:
            tiles[k] = add_boss(tiles[k], x, y)
    # tabs en costuras x = +-SEAM_X (torso)  dx=4
    for yy in (40.0, 165.0):
        cz = zdeck(yy) - 1.0 - 11.0
        tiles["torso_izq"] = add_tab(tiles["torso_izq"], -SEAM_X - 2, yy, cz, 4, 16, 22, "x")
        tiles["torso_cen"] = add_tab(tiles["torso_cen"], -SEAM_X + 2, yy, cz, 4, 16, 22, "x")
        tiles["torso_cen"] = add_tab(tiles["torso_cen"], SEAM_X - 2, yy, cz, 4, 16, 22, "x")
        tiles["torso_der"] = add_tab(tiles["torso_der"], SEAM_X + 2, yy, cz, 4, 16, 22, "x")
    # tabs en costura y=0 (piernas<->torso)
    for xx, tt, lg in ((-130, "torso_izq", "pierna_izq"), (-45, "torso_cen", "pierna_izq"),
                       (45, "torso_cen", "pierna_der"), (130, "torso_der", "pierna_der")):
        tiles[tt] = add_tab(tiles[tt], xx, 2, zdeck(2) - 1 - 11, 16, 4, 22, "y")
        tiles[lg] = add_tab(tiles[lg], xx, -2, H0 - 1 - 11, 16, 4, 22, "y")
    return tiles

# ------------------------------------------------------------------ PIEZAS SUELTAS
def trocar_guide():
    """Guia de trocar: tubo ID 11.5 (para trocares 10-11 mm) + pestana de sujecion con 2 x M3."""
    g = cyl(TROC_FL_OD / 2, 0, 3).union(cyl(TROC_OD / 2, -25, 0))
    g = g.cut(cyl(TROC_ID / 2, -30, 10))
    for s in (-13, 13):
        g = g.cut(cyl(1.7, -1, 5, x=s))
    # embudo de entrada
    g = g.faces(">Z").edges("not %LINE").chamfer(1.0) if False else g
    return g

def camera_neck():
    """Cuello elevado del puerto central (blanco) con pestana de fijacion y 3 pilotos M3 en el borde."""
    n = cyl(NECK_FL_OD / 2, 0, 3).union(cyl(NECK_OD / 2 - 0.5, -8, NECK_H))
    n = n.cut(cyl(NECK_ID / 2, -30, NECK_H + 5))
    for k in range(4):
        a = math.radians(45 + 90 * k)
        n = n.cut(cyl(1.7, -1, 5, x=42 * math.cos(a), y=42 * math.sin(a)))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        n = n.cut(cyl(1.25, NECK_H - 10, NECK_H + 1, x=BC_RIM * math.cos(a), y=BC_RIM * math.sin(a)))
    return n

def collar():
    """Collar del puerto de camara (NEGRO) - anillo OD 76 / ID 44 / h 8; 3 x M3 BC 59."""
    c = cyl(38, NECK_H + 4, NECK_H + 12).cut(cyl(22, NECK_H, NECK_H + 13))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        c = c.cut(cyl(1.7, NECK_H, NECK_H + 13, x=BC_RIM * math.cos(a), y=BC_RIM * math.sin(a)))
    return c

def webcam_arm():
    """Brazo + placa anular (OD 64/ID 44, 3 ranuras de giro +-20 deg = eje PAN) + horquilla de cabeceo (eje PITCH, M4)."""
    plate = cyl(NECK_OD / 2 - 0.5, NECK_H, NECK_H + 4).cut(cyl(22, NECK_H - 1, NECK_H + 5))
    for k in range(3):
        a0 = 90 + 120 * k
        for d in range(-20, 21, 5):
            a = math.radians(a0 + d)
            plate = plate.cut(cyl(1.7, NECK_H - 1, NECK_H + 5, x=BC_RIM * math.cos(a), y=BC_RIM * math.sin(a)))
    arm = box(-9, 9, -25, -21, -48, NECK_H + 2)
    pivot_y, pivot_z = -23.0, -48.0
    for sx in (-7.5, 7.5):
        ear = cq.Workplane("YZ").workplane(offset=sx - 1.5).center(pivot_y, pivot_z).circle(7).extrude(3)
        arm = arm.union(ear)
    hole = cq.Workplane("YZ").center(pivot_y, pivot_z).circle(2.1).extrude(30, both=True)
    return plate.union(arm).cut(hole)

def webcam_cradle(cam_w=66.0):
    """Cuna/clip para webcam (cam_w ajustable; VERIFICAR con webcam real). Pivote en la horquilla (M4)."""
    pivot_y, pivot_z = -23.0, -48.0
    lug = cq.Workplane("YZ").workplane(offset=-6).center(pivot_y, pivot_z).circle(7).extrude(12)
    plate = box(-(cam_w / 2 + 3), cam_w / 2 + 3, -17, -14, pivot_z - 34, pivot_z - 2)
    ledge = box(-(cam_w / 2 + 3), cam_w / 2 + 3, -40, -14, pivot_z - 37, pivot_z - 34)
    lips = box(-(cam_w / 2 + 3), -cam_w / 2, -40, -14, pivot_z - 37, pivot_z - 14).union(
           box(cam_w / 2, cam_w / 2 + 3, -40, -14, pivot_z - 37, pivot_z - 14))
    stem = box(-6, 6, -23, -14, pivot_z - 8, pivot_z)
    c = lug.union(plate).union(ledge).union(lips).union(stem)
    hole = cq.Workplane("YZ").center(pivot_y, pivot_z).circle(2.1).extrude(30, both=True)
    return c.cut(hole)

def corner_connector(t=PANEL_T, c=0.2, size=26.0, off=2.0):
    """Conector esquinero 90 (vertice 3 vias) para paneles de 4 mm: 3 ranuras ortogonales."""
    s = size
    body_ = box(0, s, 0, s, 0, s)
    g = t + c
    slabs = [box(off, s + 1, off, s - 4, off, off + g),      # panel XY entra por +x
             box(off, s - 4, off, off + g, off, s + 1),      # panel XZ entra por +z
             box(off, off + g, off, s + 1, off, s - 4)]      # panel YZ entra por +y
    for sl in slabs:
        body_ = body_.cut(sl)
    return body_

def base_plate():
    """Placa base MDF/acrilico 4 mm con contorno de la planta + 10 agujeros M3 (mismos que los bosses)."""
    p = box(-W / 2, W / 2, 0, L_T, 0, PANEL_T)
    try:
        p = p.edges("|Z").edges(">Y").fillet(FIL)
    except Exception:
        pass
    for sgn in (1, -1):
        xa, xb = sorted((sgn * LEG_X0, sgn * LEG_X1))
        leg = box(xa, xb, -LEG_L, 1, 0, PANEL_T)
        try:
            leg = leg.edges("|Z").edges("<Y").fillet(FIL)
        except Exception:
            pass
        p = p.union(leg)
    for lst in BOSSES.values():
        for (x, y) in lst:
            p = p.cut(cyl(1.6, -1, PANEL_T + 1, x=x, y=y))
    p = p.cut(box(-15, 15, 20, 40, -1, PANEL_T + 1))  # pasacables
    return p

# ------------------------------------------------------------------ MAIN
def export(name, wp):
    cq.exporters.export(wp, str(OUT / f"{name}.step"))
    cq.exporters.export(wp, str(OUT / f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)

def bbox(wp):
    b = wp.val().BoundingBox()
    return [round(b.xlen, 1), round(b.ylen, 1), round(b.zlen, 1)]

def bed_fit(wp):
    """Orienta con la cubierta contra la cama (rotar -A y voltear) y devuelve bbox."""
    r = wp.rotate((0, 0, 0), (1, 0, 0), -A).rotate((0, 0, 0), (1, 0, 0), 180)
    return bbox(r)

def main():
    report = {"params": dict(A=A, W=W, L_T=L_T, LEG_L=LEG_L, H0=H0, WALL=WALL), "parts": {}}
    shell = build_shell()
    tiles = build_tiles(shell)
    for k, t in tiles.items():
        export(f"carcasa_{k}", t)
    parts = {
        "guia_trocar": trocar_guide(), "cuello_camara": camera_neck(), "collar_camara_NEGRO": collar(),
        "webcam_brazo": webcam_arm(), "webcam_cuna": webcam_cradle(), "conector_esquinero_90": corner_connector(),
        "placa_base_4mm": base_plate(),
    }
    for k, p in parts.items():
        export(k, p)
    # DXF 2D de la placa base para corte laser/CNC (contorno + 10 agujeros M3 + pasacables)
    cq.exporters.export(parts["placa_base_4mm"].faces("<Z"), str(OUT / "placa_base_4mm.dxf"))
    allp = {**{f"carcasa_{k}": v for k, v in tiles.items()}, **parts}
    for k, p in allp.items():
        v = p.val()
        entry = {"valid": bool(v.isValid()), "solids": len(p.solids().vals()), "bbox_mm": bbox(p),
                 "volume_cm3": round(v.Volume() / 1000, 1), "mass_PLA_g": round(v.Volume() * PLA_DENS, 1)}
        if k.startswith("carcasa_pierna"):
            bf = bbox(p.rotate((0, 0, 0), (1, 0, 0), 180))
            entry["impresion"] = "cubierta sobre la cama (boca abajo), sin soportes"
            entry["bbox_impresion"] = bf
            entry["cabe_en_cama"] = bool(bf[0] <= BED and bf[1] <= BED)
        elif k.startswith("carcasa_torso"):
            bb = bbox(p)
            entry["impresion"] = "base abierta sobre la cama + soportes bajo la cubierta inclinada 15 deg"
            entry["bbox_impresion"] = bb
            entry["cabe_en_cama"] = bool(bb[0] <= BED and bb[1] <= BED)
        report["parts"][k] = entry
    # angulo de manipulacion entre los 2 trocares principales hacia un blanco en el piso del area de trabajo
    tgt = (0.0, 110.0, 15.0)
    def vec(p):
        x, y = p
        return (tgt[0] - x, tgt[1] - y, tgt[2] - zdeck(y))
    v1, v2 = vec(PORTS[0]), vec(PORTS[1])
    dot = sum(a * b for a, b in zip(v1, v2))
    n = math.sqrt(sum(a * a for a in v1)) * math.sqrt(sum(a * a for a in v2))
    report["angulo_manipulacion_deg"] = round(math.degrees(math.acos(dot / n)), 1)
    report["longitud_trayecto_instrumento_mm"] = round(math.sqrt(sum(a * a for a in v1)), 1)
    report["total_PLA_g"] = round(sum(v["mass_PLA_g"] for k, v in report["parts"].items()
                                      if k not in ("placa_base_4mm",)), 1)
    # ensamble completo (STEP con colores) para Onshape
    asm = cq.Assembly(name="LE1100_replica")
    white, black, wood = cq.Color(0.95, 0.95, 0.95), cq.Color(0.05, 0.05, 0.05), cq.Color(0.7, 0.55, 0.35)
    for k, t in tiles.items():
        asm.add(t, name=f"carcasa_{k}", color=white)
    for i, (x, y) in enumerate(PORTS):
        asm.add(on_deck(trocar_guide(), x, y), name=f"guia_trocar_{i+1}", color=white)
    cx, cy = CAM_XY
    asm.add(on_deck(camera_neck(), cx, cy), name="cuello_camara", color=white)
    asm.add(on_deck(collar(), cx, cy), name="collar_camara", color=black)
    asm.add(on_deck(webcam_arm(), cx, cy), name="webcam_brazo", color=cq.Color(0.4, 0.4, 0.45))
    asm.add(on_deck(webcam_cradle(), cx, cy), name="webcam_cuna", color=cq.Color(0.4, 0.4, 0.45))
    asm.add(parts["placa_base_4mm"].translate((0, 0, -PANEL_T)), name="placa_base", color=wood)
    asm.save(str(OUT / "ensamble_LE1100.step"))
    (OUT / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
