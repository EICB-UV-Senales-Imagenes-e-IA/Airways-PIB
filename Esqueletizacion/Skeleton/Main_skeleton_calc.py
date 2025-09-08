import Skeleton as ch
import helpers as fn

# Step 1: From nifti to inr (with resize)---------------------------------------
path = '../raw-data/INRS2/18/18STD_ESP'
ch.niiCut(f'{path}.nii.gz', f'{path}_cut')
ch.nii2inr(f'{path}_cut.nii.gz', f'{path}_cut')
print(f'{path}.inr save')

# Step 2: run in terminal mesh_a_3d_gary_image.cpp------------------------------

# Step 3: smooth mesh surface---------------------------------------------------
ch.HC_Laplacian_Smoothing(path+'_out.off', [0.3, 1., 3])
print('Laplacian smoothing: Done')

# Step 4: run in terminal simple_mcfskel_example.cpp----------------------------

# Step 5: create skeleton ------------------------------------------------------
fn.off2vtu(path+'_out.off',path+'_mesht.vtu')

path_nifti = f'{path}_cut.nii.gz'
affine, airway, perim = fn.geometry(path_nifti)
patient_info = ch.patient_skeleton(path, affine)#, surface = perim
patient_skel = (patient_info[0], patient_info[1], patient_info[-1])
