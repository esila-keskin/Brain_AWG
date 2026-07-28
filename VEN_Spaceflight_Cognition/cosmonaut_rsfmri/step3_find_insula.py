"""
STEP 3 is to find clusters in the normalised map and check which ones are insula.
Prints MNI coordinates of every cluster so you can identify the insula ones.
Also checks overlap with the Harvard-Oxford insula atlas region.
"""
import os
import numpy as np
import nibabel as nib
from scipy.ndimage import label
from nilearn import datasets, image as nli

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

normalised_map = os.path.join(DATA_DIR, "spmT_0001_2.nii.gz")
img = nib.load(normalised_map)
data = img.get_fdata()
affine = img.affine

THRESHOLD = 2.5

# Find all clusters above threshold
mask_pos = data > THRESHOLD   # positive clusters (increased connectivity)
mask_neg = data < -THRESHOLD  # negative clusters (decreased connectivity)

print(f"Normalised ICC map - clusters at |t| > {THRESHOLD}")

for sign, mask, label_str in [("+", mask_pos, "INCREASED connectivity after spaceflight (normalises)"),
                              ("-", mask_neg, "DECREASED connectivity after spaceflight (normalises)")]:
    labeled, n = label(mask)
    print(f"\n{label_str}")
    print(f"  {n} clusters found")
    # Only report clusters > 10 voxels
    for cid in range(1, n + 1):
        cmask = labeled == cid
        sz = int(np.sum(cmask))
        if sz < 10:
            continue
        vals = data * cmask
        if sign == "+":
            peak_vox = np.unravel_index(np.argmax(vals), vals.shape)
        else:
            peak_vox = np.unravel_index(np.argmin(vals), vals.shape)
        peak_mni = nib.affines.apply_affine(affine, np.array(peak_vox))
        peak_t = data[peak_vox]
        print(f"  Cluster {cid}: {sz:4d} voxels | "
              f"peak MNI = ({peak_mni[0]:+.0f}, {peak_mni[1]:+.0f}, {peak_mni[2]:+.0f}) | "
              f"peak t = {peak_t:+.2f}")

# Insula overlap using Harvard-Oxford atlas
print("Insula overlap (Harvard-Oxford cortical atlas)")
 
try:
    atlas = datasets.fetch_atlas_harvard_oxford("cort-maxprob-thr25-2mm")
    atlas_img = nib.load(atlas.maps)
    labels = atlas.labels

    insula_idx = [i for i, l in enumerate(labels) if "insul" in l.lower()]
    print(f"Insula label(s): {[(i, labels[i]) for i in insula_idx]}")

    atlas_data = atlas_img.get_fdata()
    insula_mask = np.isin(atlas_data, insula_idx)

    # Resample T-map to atlas space
    resampled = nli.resample_img(img,
                                 target_affine=atlas_img.affine,
                                 target_shape=atlas_img.shape[:3],
                                 interpolation="linear")
    res_data = resampled.get_fdata()

    sig = np.abs(res_data) > THRESHOLD
    insula_sig = sig & insula_mask

    print(f"Significant voxels (|t|>{THRESHOLD}): {int(np.sum(sig))}")
    print(f"  Of those, in insula: {int(np.sum(insula_sig))}")
    if np.sum(sig) > 0:
        print(f"  Insula fraction of sig. effect: {100*np.sum(insula_sig)/np.sum(sig):.1f}%")

except Exception as e:
    print(f"Atlas download failed (needs internet): {e}")
    print("Skip this section, cluster coordinates above are enough.")

print("\nDone. Use the MNI coordinates above to cite specific insula clusters.")
print("Insula is typically at MNI x = ±38, y = +2, z = 0 to +15")
