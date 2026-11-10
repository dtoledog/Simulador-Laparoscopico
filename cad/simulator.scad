// Simulador laparoscopico bajo costo - torso con piernas (replica funcional tipo LE-1100)
// Equivalente OpenSCAD de cad/simulator.py (misma geometria / parametros).
// ESTADO: NO EJECUTADO (OpenSCAD no instalado en el equipo de desarrollo). La version validada es simulator.py (STEP).
// Onshape NO abre .scad: renderizar -> exportar STL -> importar (malla no editable). Preferir los STEP de cad/out/.
$fn = 64;

// ---------------- PARAMETROS (mm) ----------------
A        = 15;      // inclinacion de cubierta (deg)
W        = 340;     // ancho torso
L_T      = 205;     // largo torso
LEG_L    = 200;     // largo piernas
LEG_X0   = 10;  LEG_X1 = 160;
H0       = 90;      // altura cubierta en y=0 y piernas
WALL     = 2.5;     // pared
SEAM_X   = 100;     // costuras torso
CAM_XY   = [0, 140];
PORTS    = [[-55, 60], [55, 60], [135, 135]];
PANEL_T  = 4;       // MDF/acrilico
TROC_ID  = 11.5; TROC_OD = 20; TROC_FL = 34;
NECK_OD  = 66; NECK_ID = 52; NECK_H = 35; NECK_FL = 94; BC_RIM = 29.5;

function zdeck(y, t = 0) = H0 + y * tan(A) - t / cos(A);

// ---------------- CARCASA ----------------
module torso_solid(t = 0) {
    y0 = (t == 0) ? 0 : t;  y1 = L_T - t;  z0 = (t == 0) ? 0 : -1;
    rotate([90, 0, 90])   // extruye el perfil (y,z) a lo largo de x
        linear_extrude(height = W - 2 * t, center = true)
            polygon([[y0, z0], [y1, z0], [y1, zdeck(y1, t)], [y0, zdeck(y0, t)]]);
}
module legs_solid(t = 0) {
    z0 = (t == 0) ? 0 : -1;  yt = (t == 0) ? 1 : t + 1;
    for (s = [1, -1])
        translate([s > 0 ? LEG_X0 + t : -(LEG_X1 - t), -LEG_L + t, z0])
            cube([LEG_X1 - LEG_X0 - 2 * t, LEG_L - t + yt, H0 - t - z0]);
}
module on_deck(x, y) { translate([x, y, zdeck(y)]) rotate([A, 0, 0]) children(); }

module shell() {
    difference() {
        union() { torso_solid(0); legs_solid(0); }
        union() { torso_solid(WALL); legs_solid(WALL); }
        for (p = PORTS) on_deck(p[0], p[1]) {
            translate([0, 0, -40]) cylinder(d = 21, h = 60);
            for (s = [-13, 13]) translate([s, 0, -40]) cylinder(d = 3.4, h = 60);
        }
        on_deck(CAM_XY[0], CAM_XY[1]) {
            translate([0, 0, -40]) cylinder(d = 75, h = 60);
            for (k = [0:3]) rotate(45 + 90 * k) translate([42, 0, -40]) cylinder(d = 3.4, h = 60);
        }
        // panel frontal pierna derecha: boton 12, USB-C 14x7.2, HDMI 16x7.6 (VERIFICAR con piezas reales)
        translate([40, -LEG_L - 1, 45]) rotate([-90, 0, 0]) cylinder(d = 12.2, h = 8);
        translate([75 - 7, -LEG_L - 1, 45 - 3.6]) cube([14, 7, 7.2]);
        translate([115 - 8, -LEG_L - 1, 45 - 3.8]) cube([16, 7, 7.6]);
    }
}
// Tiles de impresion (cortes en x=+-SEAM_X y y=0)
module tile(x0, x1, y0, y1) {
    intersection() { shell(); translate([x0, y0, -10]) cube([x1 - x0, y1 - y0, 400]); }
}
module tile_torso_izq() tile(-400, -SEAM_X, 0, 400);
module tile_torso_cen() tile(-SEAM_X, SEAM_X, 0, 400);
module tile_torso_der() tile(SEAM_X, 400, 0, 400);
module tile_pierna_izq() tile(-400, 0, -400, 0);
module tile_pierna_der() tile(0, 400, -400, 0);

// ---------------- PIEZAS ----------------
module trocar_guide() {   // a) guia de trocar Ø int 11.5 + pestana de sujecion 2xM3
    difference() {
        union() { cylinder(d = TROC_FL, h = 3); translate([0, 0, -25]) cylinder(d = TROC_OD, h = 25); }
        translate([0, 0, -30]) cylinder(d = TROC_ID, h = 40);
        for (s = [-13, 13]) translate([s, 0, -1]) cylinder(d = 3.4, h = 6);
    }
}
module camera_neck() {    // b) cuello elevado puerto de camara
    difference() {
        union() { cylinder(d = NECK_FL, h = 3); translate([0, 0, -8]) cylinder(d = NECK_OD - 1, h = NECK_H + 8); }
        translate([0, 0, -30]) cylinder(d = NECK_ID, h = NECK_H + 40);
        for (k = [0:3]) rotate(45 + 90 * k) translate([42, 0, -1]) cylinder(d = 3.4, h = 6);
        for (k = [0:2]) rotate(90 + 120 * k) translate([BC_RIM, 0, NECK_H - 10]) cylinder(d = 2.5, h = 11);
    }
}
module collar() {         // collar NEGRO
    translate([0, 0, NECK_H + 4]) difference() {
        cylinder(d = 76, h = 8);
        translate([0, 0, -1]) cylinder(d = 44, h = 10);
        for (k = [0:2]) rotate(90 + 120 * k) translate([BC_RIM, 0, -1]) cylinder(d = 3.4, h = 10);
    }
}
module corner_connector(t = PANEL_T, c = 0.2, s = 26, off = 2) {   // c) conector esquinero 90 grados, 3 ranuras
    g = t + c;
    difference() {
        cube([s, s, s]);
        translate([off, off, off]) cube([s, s - 4 - off, g]);
        translate([off, off, off]) cube([s - 4 - off, g, s]);
        translate([off, off, off]) cube([g, s, s - 4 - off]);
    }
}
module webcam_arm() {     // d) brazo + placa con ranuras de giro (PAN) + horquilla de cabeceo (PITCH, M4)
    difference() {
        union() {
            translate([0, 0, NECK_H]) cylinder(d = NECK_OD - 2, h = 4);
            translate([-9, -25, -48]) cube([18, 4, NECK_H + 50]);
            for (sx = [-7.5, 7.5]) translate([sx - 1.5, -23, -48]) rotate([0, 90, 0]) cylinder(r = 7, h = 3);
        }
        translate([0, 0, NECK_H - 1]) cylinder(d = 44, h = 6);
        for (k = [0:2]) for (d = [-20:5:20]) rotate(90 + 120 * k + d) translate([BC_RIM, 0, NECK_H - 1]) cylinder(d = 3.4, h = 6);
        translate([-20, -23, -48]) rotate([0, 90, 0]) cylinder(d = 4.2, h = 40);
    }
}
module webcam_cradle(cam_w = 66) {   // cuna ajustable (VERIFICAR con webcam real)
    difference() {
        union() {
            translate([-6, -23, -48]) rotate([0, 90, 0]) cylinder(r = 7, h = 12);
            translate([-(cam_w / 2 + 3), -17, -82]) cube([cam_w + 6, 3, 32]);
            translate([-(cam_w / 2 + 3), -40, -85]) cube([cam_w + 6, 26, 3]);
            for (sx = [-(cam_w / 2 + 3), cam_w / 2]) translate([sx, -40, -85]) cube([3, 26, 23]);
            translate([-6, -23, -56]) cube([12, 9, 8]);
        }
        translate([-20, -23, -48]) rotate([0, 90, 0]) cylinder(d = 4.2, h = 40);
    }
}
module base_plate() {     // e) placa base MDF/acrilico 4 mm (corte laser/CNC)
    linear_extrude(PANEL_T) union() {
        translate([-W / 2, 0]) square([W, L_T]);
        for (s = [1, -1]) translate([s > 0 ? LEG_X0 : -LEG_X1, -LEG_L]) square([LEG_X1 - LEG_X0, LEG_L + 1]);
    }
}

// ---------------- VISTA (descomentar una) ----------------
tile_torso_cen();
// tile_torso_izq(); tile_torso_der(); tile_pierna_izq(); tile_pierna_der();
// trocar_guide(); camera_neck(); collar(); webcam_arm(); webcam_cradle(); corner_connector(); base_plate();
