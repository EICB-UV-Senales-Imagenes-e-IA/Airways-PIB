import numpy as np
import nibabel as nib
import pyvista as pv
import os

# Configurar rutas
seg_manual = "ATM_001_0000.nii.gz"
seg_auto = "ATM_001_0000 segmentation.nii.gz"


# Cargar volúmenes
print(f"Cargando volumenes de máscaras binarias")
gt = nib.load(seg_manual).get_fdata().astype(bool)
pred = nib.load(seg_auto).get_fdata().astype(bool)


# Crear máscaras
print(f"Creando mascaras")
TP = np.logical_and(pred, gt)
FP = np.logical_and(pred, ~gt)
FN = np.logical_and(~pred, gt)

# Liberar memoria de arrays grandes inmediatamente
del pred, gt

print(f"Creando superficies 3D")
# Crear superficies 3D
tp_volume = pv.wrap(TP.astype(np.uint8))
tp_surf = tp_volume.contour()

fp_volume = pv.wrap(FP.astype(np.uint8))
fp_surf = fp_volume.contour()

fn_volume = pv.wrap(FN.astype(np.uint8))
fn_surf = fn_volume.contour()

# Liberar máscaras inmediatamente
del TP, FP, FN

# Crear plotter
print(f"Creando plotter...")
plotter = pv.Plotter(window_size=[1000, 800])
plotter.set_background('white')
print(f"Listo, creando superficies inciales")


# Añadir superficies iniciales
actor_tp = plotter.add_mesh(tp_surf, color="#f0ea3c", opacity=0.95, name="TP",
                            smooth_shading=True, specular=0.6, specular_power=80)
actor_fp = plotter.add_mesh(fp_surf, color='#ab0100', opacity=0.95, name="FP")
actor_fn = plotter.add_mesh(fn_surf, color='#3c75ab', opacity=0.95, name="FN")

# Callbacks para controles interactivos

print(f"Listo")


def toggle_tp(state):
    actor_tp.SetVisibility(state)


def toggle_fp(state):
    actor_fp.SetVisibility(state)


def toggle_fn(state):
    actor_fn.SetVisibility(state)


def set_opacity(value):
    actor_tp.GetProperty().SetOpacity(value)
    actor_fp.GetProperty().SetOpacity(value)
    actor_fn.GetProperty().SetOpacity(value)


# Añadir widgets al visualizador
plotter.add_text("Visualización de Vías Aéreas",
                 position="upper_edge", font_size=12, color="black")

plotter.add_checkbox_button_widget(
    toggle_tp, position=(10, 100), size=15, value=True)
plotter.add_text("TP (Amarillo)", position=(
    40, 100), font_size=9, color="black")

plotter.add_checkbox_button_widget(
    toggle_fp, position=(10, 70), size=15, value=True)
plotter.add_text("FP (Rojo)", position=(40, 70), font_size=9, color="black")

plotter.add_checkbox_button_widget(
    toggle_fn, position=(10, 40), size=15, value=True)
plotter.add_text("FN (Azul)", position=(40, 40), font_size=9, color="black")

slider = plotter.add_slider_widget(
    set_opacity,
    rng=[0.1, 1.0],
    value=1.00,
    pointa=(0.9, 0.4),
    pointb=(0.9, 0.9),
    title="Opacidad",
    title_color="black",
    title_height=0.3,
    fmt="%.2f",
    color="gray"
)
# Mostrar vis
plotter.show()
