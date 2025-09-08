import os
import subprocess
import Skeleton as ch
import helpers as fn
from collections import Counter, defaultdict
import csv
import time

start_time = time.time()

# Paths base
build_dir = os.path.join(os.path.dirname(__file__), "build")
all_data = defaultdict(dict)

# Lista de casos a procesar
"""
Hecho con 30 pacientes, actualizado 2.0. Hay que tener ojo con las primeras 3 generaciones
 = [
    #"./Data/Airways/ATM_"+f'{i:03d}_0000/ATM_'+f'{i:03d}_0000' for i in range(1, 31)
    
    # ... agrega todos los paths que quieras procesar

    #"./Data/results/ATM_"+f'{i:03d}_0000 segmentation' for i in range(1, 31)
]
"""
paths = [
    #"./Data/results/ATM_"+f'{i:03d}_0000 segmentation' for i in range(1, 31),
    "./Data/results/ATM_"+f'{i:03d}_0000 segmentation/ATM_'+f'{i:03d}_0000 segmentation' for i in range(1, 31)

    ] 
# ... agrega todos los paths que quieras procesar, sin extension

for path in paths:
    print(f'Procesando {path}...')
    # Paso 1: NIfTI → INR
    ch.niiCut(f'{path}.nii.gz', f'{path}_cut')
    ch.nii2inr(f'{path}_cut.nii.gz', f'{path}_cut')
    print(f'{path}.inr save')

    # Paso 2: Mesh (INR → OFF)
    input_inr = f'{path}_cut.inr'
    output_off = f'{path}_out.off'
    mesh_exe = os.path.join(build_dir, "mesh_a_3d_gray_image")
    subprocess.run([mesh_exe, input_inr, output_off], check=True)

    # Paso 3: Suavizado
    ch.HC_Laplacian_Smoothing(output_off, [0.6, 1, 3])
    print('Laplacian smoothing: Done')

    # Paso 4: Skeleton (OFF → skeleton)
    skel_exe = os.path.join(build_dir, "simple_mcfskel_example")
    output_base = f'{path}'
    input_inr = f'{path}_cut.inr'
    subprocess.run([skel_exe, output_off, output_base], check=True)
    # Salidas: {path}_skel-sm.polylines.txt, {path}_correspondance-sm.polylines.txt

    # Paso 5: Exportar VTU u otros procesos
    fn.off2vtu(output_off, f'{path}_mesht.vtu')

    # Paso 6: Post-procesamiento Python (opcional)
    path_nifti = f'{path}_cut.nii.gz'
    affine, airway, perim = fn.geometry(path_nifti)
    patient_info = ch.patient_skeleton(path, affine) #[0] estan los branches
    
    ##  Paso 7: Contar ramas por generación
    generations = [branch.generation for branch in patient_info[0]]
    generation_counts = Counter(generations)
    # Guardar conteos para cada paciente
    paciente_id = os.path.basename(path)
    all_data[paciente_id] = {
    **{f'Gen_{gen}': count for gen, count in generation_counts.items()}
        }
    #break

# Escribir CSV, modifica el nombre segun lo que proceses
with open('conteo_metodo_automatico.csv', 'w', newline='') as f:
    # Obtener todas las generaciones únicas encontradas
    all_generations = sorted({
        gen for data in all_data.values() 
        for gen in data.keys() if gen.startswith('Gen_')
    })
    
    fieldnames = ['Paciente'] + all_generations
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for paciente, data in all_data.items():
        row = {'Paciente': paciente, **data}
        writer.writerow(row)



# --- Fin del cronómetro ---
total_time = time.time() - start_time


print(f"\n⏳ Tiempo total de ejecución: {int(total_time//60)} minutos y {int(total_time%60)} segundos")










    # print("Conteo de ramas por generación:")
    # for gen, count in sorted(generation_counts.items()):
    #     print(f"Generación {gen}: {count} ramas")
    # #Total ramas
    # total_ramas = len(generations)
    # print(f"Total de vías aéreas (ramas): {total_ramas}")
    
    # print(f'Finalizado {path}\n')
    # break
